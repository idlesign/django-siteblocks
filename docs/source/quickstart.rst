Getting started
===============

.. _tag-quickstart:

* Add the **siteblocks** application to INSTALLED_APPS in your settings file (usually 'settings.py').
* Use ``> python manage.py migrate`` command to install app tables into DB.
* Make sure `TEMPLATE_CONTEXT_PROCESSORS` in your settings file has `django.core.context_processors.request` if you want to use static blocks created in Django Admin.
  For Django 1.8+: `django.template.context_processors.request` should be defined in ``TEMPLATES/OPTIONS/context_processors``.


Quick example
-------------

.. note::

    This example covers only static siteblocks. More advanced technique can be found in :ref:`Dynamic siteblocks <tag-dynamic>` section.


Let's say we need random quotes block.

1. Add `{% siteblock "my_quotes" %}` tag where you need it in templates. Here ``my_quotes`` is the alias of a block.

    .. code-block:: html

        {% extends "_base.html" %}
        {% load siteblocks %}

        {% block sidebar %}
            <div class="quote">
                {% siteblock "my_quotes" %}
            </div>
        {% endblock %}


    .. note::

       You can use `{% siteblock "my_quotes" as my_var %}` tag variation to put block contents into a template context variable.


2. Go to Django Admin site and add several siteblocks with quotes aliased `my_quotes`.

   *Note that you can render different sets of quotes on different pages (URLs or views).*


Random quotes are here. You're done.
