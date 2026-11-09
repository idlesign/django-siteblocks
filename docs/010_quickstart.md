# Getting started

* Add the **siteblocks** application to `INSTALLED_APPS` in your settings file (usually `settings.py`).
* Use `> python manage.py migrate` command to install app tables into DB.
* Make sure `context_processors` in `TEMPLATES/OPTIONS` of your settings file has `django.template.context_processors.request` if you want to use static blocks created in Django Admin.

## Quick example

!!! note

    This example covers only static siteblocks. More advanced technique can be found in [Dynamic siteblocks](020_dynamic.md) section.

Let's say we need random quotes block.

1. Add `{% siteblock "my_quotes" %}` tag where you need it in templates. Here `my_quotes` is the alias of a block.

    ```html
    {% extends "_base.html" %}
    {% load siteblocks %}

    {% block sidebar %}
        <div class="quote">
            {% siteblock "my_quotes" %}
        </div>
    {% endblock %}
    ```

    !!! note

        You can use `{% siteblock "my_quotes" as my_var %}` tag variation to put block contents into a template context variable.

2. Go to Django Admin site and add several siteblocks with quotes aliased `my_quotes`.

    *Note that you can render different sets of quotes on different pages (URLs or views).*

Random quotes are here. You're done.
