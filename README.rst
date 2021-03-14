django-polymorphic-foreignkey
=============================

Testing
-------

In order to execute local tox tests, do::

    $ python -m venv venv
    $ . venv/bin/activate
    $ pip install tox
    $ tox -- --selenium=chrome-headless


or a specific environment configuration::

    $ tox -e py37-dj31 -- --selenium=chrome-headless
