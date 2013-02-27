SiteBlocks for Django
=======================================
http://github.com/idlesign/django-siteblocks

What's that
-----------
django-siteblocks is a reusable application for Django introducing blocks of static data (also known as flatblocks) that could be used in templates. These blocks are rendered in templates dependant on current URL.

Requirements
------------
1.  Django 1.1+
2. 'Admin site' Django contrib package

How to use
----------

1. Add the 'siteblocks' application to 'INSTALLED_APPS' in your settings file (usually 'settings.py').
2. Run './manage.py syncdb' to install siteblocks table into database.
3. Go to Django Admin site and add some site blocks.
4. Add '{% load siteblocks %}' tag to the top of a template.
5. Add '{% siteblock "myblock" %}' tag where you need it in template. Here 'myblock' is the alias of a block. **NB**: You can always put into quotes a template variable.

Use '{% siteblock "myblock" as myvar %}' tag notation to put block contents into 'myvar' variable instead of rendering.

Translating django-siteblocks
-----------------------------
You can translate application into your language if it is supported by Django.  
For translation tips refer to Django documentation: http://docs.djangoproject.com/en/1.1/topics/i18n/localization/
