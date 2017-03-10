from __future__ import absolute_import

import json
import logging

from django_admin_testutils import AdminSeleniumTestCase


logger = logging.getLogger(__name__)


class BasePolymorphicForeignKeyTestCase(AdminSeleniumTestCase):

    root_urlconf = 'polymorphic_fk.tests.urls'

    def save_form(self):
        browser_errors = [e for e in self.selenium.get_log('browser')
                          if 'favicon' not in e['message']]
        if len(browser_errors) > 0:
            logger.error("Found browser errors: %s" % json.dumps(browser_errors, indent=4))
        super(BasePolymorphicForeignKeyTestCase, self).save_form()
