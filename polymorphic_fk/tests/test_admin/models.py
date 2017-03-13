try:
    # Django 1.10
    from django.urls import reverse
except ImportError:
    # Django <= 1.9
    from django.core.urlresolvers import reverse

import django
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six

from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from polymorphic_fk.fields import PolymorphicForeignKey


class AdminLinkMixin(object):

    @classmethod
    def get_admin_changelist_url(cls):
        info = (cls._meta.app_label, cls._meta.model_name)
        return reverse("admin:%s_%s_changelist" % info)

    @classmethod
    def get_admin_add_url(cls):
        info = (cls._meta.app_label, cls._meta.model_name)
        return reverse("admin:%s_%s_add" % info)

    def get_admin_change_url(self):
        info = (type(self)._meta.app_label, type(self)._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=[self.pk])


@python_2_unicode_compatible
class Base(AdminLinkMixin, PolymorphicModel):
    slug = models.SlugField()
    objects = PolymorphicManager()

    class Meta:
        if django.VERSION > (1, 10):
            manager_inheritance_from_future = True

    def __str__(self):
        return "Base %s" % self.slug


@python_2_unicode_compatible
class A(Base):
    a_val = models.CharField(max_length=32)

    class Meta:
        if django.VERSION > (1, 10):
            manager_inheritance_from_future = True

    def __str__(self):
        text_method = '__str__' if six.PY3 else '__unicode__'
        return "A(%s) <%s>" % (self.a_val, getattr(super(A, self), text_method)())


@python_2_unicode_compatible
class B(Base):
    b_val = models.CharField(max_length=32)

    class Meta:
        if django.VERSION > (1, 10):
            manager_inheritance_from_future = True

    def __str__(self):
        text_method = '__str__' if six.PY3 else '__unicode__'
        return "B(%s) <%s>" % (self.b_val, getattr(super(B, self), text_method)())


@python_2_unicode_compatible
class C(Base):
    c_val = models.CharField(max_length=32)

    class Meta:
        if django.VERSION > (1, 10):
            manager_inheritance_from_future = True

    def __str__(self):
        text_method = '__str__' if six.PY3 else '__unicode__'
        return "C(%s) <%s>" % (self.c_val, getattr(super(C, self), text_method)())


@python_2_unicode_compatible
class Group(AdminLinkMixin, models.Model):
    slug = models.SlugField()

    def __str__(self):
        return "Group(%s)" % self.slug


@python_2_unicode_compatible
class Item(AdminLinkMixin, models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField()
    fk = PolymorphicForeignKey(Base, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        s = "Item(%s)" % self.slug
        if self.group:
            s = "%s %s" % (s, self.group)
        return "%s => %s" % (s, self.fk)
