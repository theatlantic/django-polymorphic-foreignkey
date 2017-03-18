from django.contrib.contenttypes.models import ContentType
from django.utils.six.moves import range

from selenium.webdriver.support.ui import Select

from polymorphic_fk.tests.base import BasePolymorphicForeignKeyTestCase

from .models import A, B, C, Item, Group


class PolymorphicForeignKeyAdminTestCase(BasePolymorphicForeignKeyTestCase):

    def setUp(self):
        super(PolymorphicForeignKeyAdminTestCase, self).setUp()
        self.group = Group.objects.create(slug='group')
        n = 0
        for i, model_cls in enumerate((A, B, C)):
            attr = model_cls.__name__.lower()
            for j in range(0, 3 - i):
                slug = "%s-%d" % (attr, n)
                fk = model_cls.objects.create(slug=slug, **{
                    ("%s_val" % attr): ("%d" % j)})
                Item.objects.create(
                    position=n, group=self.group, slug="item-%s" % slug, fk=fk)
                n += 1

    def test_group_contenttype_select_html(self):
        self.load_admin(self.group)
        expected_html = """
        <select class="polymorphic-ctypes" id="id_item_set-0-fk_ctypes">
            <option value=""></option>
            <option value="%(a_ctype)s" data-changelist-url="%(a_url)s"
                    selected="selected">A</option>
            <option value="%(b_ctype)s" data-changelist-url="%(b_url)s">B</option>
            <option value="%(c_ctype)s" data-changelist-url="%(c_url)s">C</option>
        </select>
        """ % {
            'a_ctype': ContentType.objects.get_for_model(A, for_concrete_model=False).pk,
            'b_ctype': ContentType.objects.get_for_model(B, for_concrete_model=False).pk,
            'c_ctype': ContentType.objects.get_for_model(C, for_concrete_model=False).pk,
            'a_url': A.get_admin_changelist_url(),
            'b_url': B.get_admin_changelist_url(),
            'c_url': C.get_admin_changelist_url(),
        }
        with self.clickable_selector('#id_item_set-0-fk_ctypes') as select:
            actual_html = self.selenium.execute_script(
                "return arguments[0].outerHTML", select)
        self.assertHTMLEqual(expected_html, actual_html)

    def test_changelist_url(self):
        self.load_admin(self.group)
        with self.clickable_selector('#lookup_id_item_set-0-fk') as el:
            lookup_link = el
        self.assertEqual(
            lookup_link.get_attribute('href'),
            "%s%s" % (self.live_server_url, A.get_admin_changelist_url()))

    def test_changelist_change_url(self):
        self.load_admin(self.group)
        with self.clickable_selector('#id_item_set-0-fk_ctypes') as el:
            select = Select(el)
            select.select_by_visible_text('B')
        self.wait_until_available_selector(
            '#lookup_id_item_set-0-fk[href="%s"]' % B.get_admin_changelist_url())

    def test_load_admin(self):
        self.load_admin(self.group)
        a_obj_pk = "%d" % A.objects.get(slug='a-0').pk
        with self.available_selector('#id_item_set-0-fk') as el:
            val = self.selenium.execute_script("return arguments[0].value", el)
        self.assertEqual(val, a_obj_pk)

    def test_save_form(self):
        b_obj = B.objects.get(slug='b-3')
        self.load_admin(self.group)
        with self.clickable_selector('#id_item_set-0-fk_ctypes') as el:
            select = Select(el)
            select.select_by_visible_text('B')
        self.wait_until_available_selector(
            '#lookup_id_item_set-0-fk[href="%s"]' % B.get_admin_changelist_url())
        with self.available_selector('#id_item_set-0-fk') as el:
            el.clear()
            el.send_keys("%d" % b_obj.pk)
        self.save_form()
        item = self.group.item_set.all()[0]
        self.assertEqual(item.fk, b_obj)
        with self.available_selector('#id_item_set-0-fk') as el:
            val = self.selenium.execute_script("return arguments[0].value", el)
        self.assertEqual(val, "%d" % b_obj.pk)
