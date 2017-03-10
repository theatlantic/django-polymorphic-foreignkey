import glob
import os

from django_admin_testutils.settings import *


current_dir = os.path.abspath(os.path.dirname(__file__))

ROOT_URLCONF = 'polymorphic_fk.tests.urls'
INSTALLED_APPS += (
    'nested_admin',
    'polymorphic',
    'polymorphic_fk',
    'polymorphic_fk.tests',
)

# Add apps within the tests folder
for p in glob.glob(os.path.join(current_dir, '*', 'models.py')):
    INSTALLED_APPS += tuple(["polymorphic_fk.tests.%s" %
        os.path.basename(os.path.dirname(p))])

LOGGING['loggers']['polymorphic_fk.tests'] = {
    'handlers': ['console'],
    'level': 'WARNING',
}
