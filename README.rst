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


What's that
-----------

*django-siteblocks is a reusable application for Django to build blocks of static or dynamic data that could be used in templates.*

It allows you to describe data that doesn't clearly belong to any application in your project in terms of static or dynamic blocks,
that could be rendered in certain places on site pages. These blocks are addressed in templates by their aliases.

The following siteblock types are supported:

Static
~~~~~~
Those are defined using Django Admin contrib and are linked to certain URLs.

This allows different siteblock contents on different URLs. Just go to admin and add some blocks.

Dynamic
~~~~~~~

Those are ordinary Python functions registered as siteblocks returning contents.

This allows complex logic to build siteblock contents. Let's make a block with a random quote from Pratchett:

.. code-block:: python

        from random import choice

        from siteblocks.siteblocksapp import register_dynamic_block


        def get_quote(**kwargs):
            quotes = [
                'Early to rise, early to bed, makes a man healthy, wealthy and dead.',
                'The duke had a mind that ticked like a clock and, like a clock, it regularly went cuckoo.',
                'Speak softly and employ a huge man with a crowbar.',
            ]
            return choice(quotes)

        register_dynamic_block('quote', get_quote)


Block rendering
---------------

Use ``siteblocks`` tag to render block contents where you need it.

.. code-block:: html

    {% load siteblocks %}

    <div class="quote">
        {% siteblock "quote" %}
    </div>


Documentation
-------------

http://django-siteblocks.readthedocs.org/
