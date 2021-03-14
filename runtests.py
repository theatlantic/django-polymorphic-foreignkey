#!/usr/bin/env python
import warnings
import selenosis


def main():
    warnings.simplefilter("error", Warning)
    warnings.filterwarnings("ignore", module="polymorphic")
    warnings.filterwarnings("ignore", "use_for_related_fields")

    try:
        from django.utils.deprecation import RemovedInDjango40Warning
    except ImportError:
        pass
    else:
        warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)

    try:
        from django.utils.deprecation import RemovedInDjango41Warning
    except ImportError:
        pass
    else:
        warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)

    # Introduced in Python 3.7
    warnings.filterwarnings(
        'ignore',
        category=DeprecationWarning,
        message="Using or importing the ABCs from 'collections' instead of from 'collections.abc'",
    )

    runtests = selenosis.RunTests("polymorphic_fk.tests.settings", "polymorphic_fk")
    runtests()


if __name__ == '__main__':
    main()
