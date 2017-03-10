#!/usr/bin/env python
import warnings
import django_admin_testutils


def main():
    warnings.simplefilter("error", Warning)
    warnings.filterwarnings("ignore", module="polymorphic")
    warnings.filterwarnings("ignore", "use_for_related_fields")
    runtests = django_admin_testutils.RunTests(
        "polymorphic_fk.tests.settings", "polymorphic_fk")
    runtests()


if __name__ == '__main__':
    main()
