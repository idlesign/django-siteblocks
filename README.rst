django-siteblocks
=================
http://github.com/idlesign/django-siteblocks

.. image:: https://pypip.in/d/django-siteblocks/badge.png
        :target: https://crate.io/packages/django-siteblocks


What's that
-----------
django-siteblocks is a reusable application for Django introducing to build blocks of static or dynamic data that could be used in templates.

These blocks are rendered in templates with different contents depending on current URL.


Requirements
------------
1. Python 2.7+ or 3.3+
2. Django 1.4+
3. Django Admin contrib enabled (optional)
4. South (for automatic DB migrations)


How to use
----------

1. Add the `siteblocks` application to `INSTALLED_APPS` in your settings file (usually `settings.py`).
2. Run `./manage.py migrate` to install siteblocks table into database.
3. Go to Django Admin site and add some site blocks.
4. Add '{% load siteblocks %}' tag to the top of a template.
5. Add '{% siteblock "myblock" %}' tag where you need it in template. Here ``myblock`` is the alias of a block.

Use '{% siteblock "myblock" as myvar %}' tag notation to put block contents into `myvar` variable instead of rendering.


Translating django-siteblocks
-----------------------------
You can translate application into your language if it is supported by Django.  
For translation tips refer to Django documentation: http://docs.djangoproject.com/en/1.1/topics/i18n/localization/



.. image:: https://d2weczhvl823v0.cloudfront.net/idlesign/django-siteblocks/trend.png
        :target: https://bitdeli.com/free
        
