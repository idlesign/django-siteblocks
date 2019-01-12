django-siteblocks
=================
http://github.com/idlesign/django-siteblocks

.. image:: https://idlesign.github.io/lbc/py2-lbc.svg
   :target: https://idlesign.github.io/lbc/
   :alt: LBC Python 2

----

.. image:: https://img.shields.io/pypi/v/django-siteblocks.svg
    :target: https://pypi.python.org/pypi/django-siteblocks

.. image:: https://img.shields.io/pypi/l/django-siteblocks.svg
    :target: https://pypi.python.org/pypi/django-siteblocks

.. image:: https://img.shields.io/coveralls/idlesign/django-siteblocks/master.svg
    :target: https://coveralls.io/r/idlesign/django-siteblocks

.. image:: https://img.shields.io/travis/idlesign/django-siteblocks/master.svg
    :target: https://travis-ci.org/idlesign/django-siteblocks

.. image:: https://landscape.io/github/idlesign/django-siteblocks/master/landscape.svg?style=flat
   :target: https://landscape.io/github/idlesign/django-siteblocks/master


What's that
-----------

*django-siteblocks is a reusable application for Django to build blocks of static or dynamic data that could be used in templates.*

It allows you to describe data that doesn't clearly belong to any application in your project in terms of static or dynamic blocks,
that could be rendered in certain places on site pages. These blocks are addressed in templates by their aliases.

Two siteblock types are supported:

* *Static.* Those are defined using Django Admin contrib and are linked to certain URLs.

  This allows different siteblock contents on different URLs.

* *Dynamic.* Those are ordinary Python functions registered as siteblocks returning contents.

  This allows complex logic to build siteblock contents.


If one and the same siteblock has more than one content associated with it, rendered content will be chosen randomly.


Documentation
-------------

http://django-siteblocks.readthedocs.org/
