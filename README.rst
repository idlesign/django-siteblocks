django-siteblocks
=================
http://github.com/idlesign/django-siteblocks

.. image:: https://pypip.in/d/django-siteblocks/badge.png
        :target: https://crate.io/packages/django-siteblocks


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

Yeah, you're right, that could be used to render random quotes on your site.


Documentation
-------------

http://django-siteblocks.readthedocs.org/



.. image:: https://d2weczhvl823v0.cloudfront.net/idlesign/django-siteblocks/trend.png
        :target: https://bitdeli.com/free
