from collections import OrderedDict
import itertools
import json

import django
from django.apps import apps
import django.contrib.admin
try:
    # Django 1.10
    from django.urls import reverse
except ImportError:
    # Django <= 1.9
    from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, Count
from django.utils import six

import monkeybiz


def compat_rel(f):
    try:
        # Django 1.9+
        return f.remote_field
    except AttributeError:
        return f.rel


def compat_rel_to(f):
    try:
        # Django 1.9+
        return f.remote_field.model
    except AttributeError:
        # Django 1.8
        return f.rel.to


@monkeybiz.patch(django.contrib.admin.ModelAdmin)
def formfield_for_foreignkey(orig, self, db_field, request=None, **kwargs):
    if isinstance(db_field, PolymorphicForeignKey):
        return db_field.formfield(request=request, admin_site=self.admin_site, **kwargs)
    return orig(self, db_field, request=request, **kwargs)


def model_shortname(model):
    opts = model._meta
    return "%s.%s" % (opts.app_label, opts.model_name)


def normalize_model(model):
    if isinstance(model, six.string_types):
        return apps.get_model(model)
    else:
        return model


class PolymorphicForeignKeyRawIdWidget(ForeignKeyRawIdWidget):

    class Media:
        js = ['admin/polymorphic_fk/polymorphic_fk.js']
        css = {'all': ['admin/polymorphic_fk/polymorphic_fk.css']}

    def render(self, name, value, attrs=None):
        attrs = {} if attrs is None else attrs
        if self.attrs:
            attrs.update(self.attrs)
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.model._default_manager.using(self.db).get(**{key: value})
        except (ValueError, self.rel.model.DoesNotExist):
            pass
        else:
            polymorphic_model = type(obj)
            attrs['data-content-type-id'] = "%s" % ContentType.objects.get_for_model(
                polymorphic_model, for_concrete_model=False).pk
        return super(PolymorphicForeignKeyRawIdWidget, self).render(name, value, attrs)


class PolymorphicForeignKey(ForeignKey):

    exclude = tuple([])
    widget_cls = PolymorphicForeignKeyRawIdWidget
    model_choices = None

    def __init__(self, to, **kwargs):
        if 'model_labels' in kwargs:
            self.model_labels = {k.lower(): v for k, v in kwargs.pop('model_labels')}
        elif not getattr(self, 'model_labels', None):
            self.model_labels = {}
        if 'exclude' in kwargs:
            self.exclude = kwargs.pop('exclude')
        if 'model_choices' in kwargs:
            self.model_choices = kwargs.pop('model_choices')
        super(PolymorphicForeignKey, self).__init__(to, **kwargs)

    def _get_model_label(self, model):
        shortname = model_shortname(model)
        if shortname in self.model_labels:
            return self.model_labels[shortname]
        else:
            return model._meta.verbose_name.title()

    def get_model_choices(self, request=None, admin_site=None, queryset=None):
        model_labels = {normalize_model(m): l for m, l in six.iteritems(self.model_labels)}
        exclude = [normalize_model(m) for m in self.exclude]
        models = []
        model_choices = []
        if self.model_choices is not None:
            for model, label in self.model_choices:
                model = normalize_model(model)
                models.append(model)
                model_labels.setdefault(model, label)
        else:
            models = []
            ctype_qset = (queryset
                .order_by()
                .exclude(polymorphic_ctype__isnull=True)
                .values('polymorphic_ctype')
                .annotate(Count('pk'))
                .order_by('-pk__count')
                .values_list('polymorphic_ctype', flat=True))
            ctypes = [ContentType.objects.get_for_id(ctid) for ctid in ctype_qset]
            app_ctypes = OrderedDict({})
            for ctype in ctypes:
                model = ctype.model_class()
                app_label = model._meta.app_label
                app_ctypes.setdefault(app_label, [])
                app_ctypes[app_label].append(ctype)
            ordered_ctypes = itertools.chain.from_iterable(six.itervalues(app_ctypes))
            for ctype in ordered_ctypes:
                models.append(ctype.model_class())

        for model in models:
            if model in exclude:
                continue
            if admin_site:
                admin = admin_site._registry.get(model)
                if not admin:
                    continue
                if request and not admin.has_change_permission(request):
                    continue
            label = model_labels.get(model) or model._meta.verbose_name.title()
            model_choices.append((model, label))

        return model_choices

    def formfield(self, request=None, admin_site=None, queryset=None, **kwargs):
        admin_site = admin_site or django.contrib.admin.site
        using = kwargs.get('using')
        if queryset is None:
            rel_to = compat_rel_to(self)
            queryset = rel_to._default_manager.using(using).non_polymorphic()
        model_choices = self.get_model_choices(
            request=request,
            admin_site=admin_site,
            queryset=queryset)
        widget_data = []
        for model, label in model_choices:
            opts = model._meta
            content_type = ContentType.objects.get_for_model(model, for_concrete_model=False)
            current_app = admin_site.name if admin_site else None
            widget_data.append({
                'content_type_id': content_type.pk,
                'label': label,
                'url': reverse(
                    "admin:%s_%s_changelist" % (opts.app_label, opts.model_name),
                    current_app=current_app),
            })
        rel = compat_rel(self)
        kwargs['widget'] = self.widget_cls(rel, admin_site, using=using, attrs={
            'data-choices': json.dumps(widget_data),
            'class': 'vForeignKeyRawIdAdminField polymorphic-fk',
        })
        return super(PolymorphicForeignKey, self).formfield(**kwargs)
