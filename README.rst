django-siteblocks
=================
http://github.com/idlesign/django-siteblocks

.. image:: https://badge.fury.io/py/django-siteblocks.png
    :target: http://badge.fury.io/py/django-siteblocks

.. image:: https://pypip.in/d/django-siteblocks/badge.png
        :target: https://crate.io/packages/django-siteblocks

.. image:: https://coveralls.io/repos/idlesign/django-siteblocks/badge.png
    :target: https://coveralls.io/r/idlesign/django-siteblocks

.. image:: https://travis-ci.org/idlesign/django-siteblocks.svg?branch=master
    :target: https://travis-ci.org/idlesign/django-siteblocks


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
