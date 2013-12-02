import re
from random import choice
from collections import defaultdict

from django.core.cache import cache
from django.core.urlresolvers import resolve, Resolver404
from django.db.models import signals

from .models import Block

# TODO dynamic blocks
# TODO + helper class (template rendering)
# TODO + context as input arg
# TODO + arbitrary dynamic block caching
# TODO + autodiscovery


# siteblocks objects are stored in Django cache for a year (60 * 60 * 24 * 365 = 31536000 sec).
# Cache is only invalidated on block item change.
CACHE_TIMEOUT = 31536000
CACHE_KEY = 'siteblocks'


class SiteBlocks(object):

    def __init__(self):
        self._cache = None
        signals.post_save.connect(self._cache_empty, sender=Block)
        signals.post_delete.connect(self._cache_empty, sender=Block)

    def _cache_init(self):
        """Initializes local cache from Django cache."""
        cache_ = cache.get(CACHE_KEY)
        if cache_ is None:
            cache_ = defaultdict(dict)
        self._cache = cache_

    def _cache_save(self):
        cache.set(CACHE_KEY, self._cache, CACHE_TIMEOUT)

    def _cache_get(self, key):
        """Returns cache entry parameter value by its name."""
        return self._cache.get(key, False)

    def _cache_set(self, key, value):
        """Replaces entire cache entry parameter data by its name with new data."""
        self._cache[key] = value

    def _cache_empty(self, **kwargs):
        self._cache = None
        cache.delete(CACHE_KEY)

    def get(self, block_alias, context):
        if 'request' not in context:
            # No use in further actions as we won't ever know current URL.
            raise SiteBlocksError('Siteblocks requires "django.core.context_processors.request" to be in TEMPLATE_CONTEXT_PROCESSORS in your settings file. If it is, check that your view pushes request data into the template.')

        current_url = context['request'].path

        # Resolve current view name to support view names as block URLs.
        try:
            resolver_match = resolve(current_url)
            namespace = ''
            if resolver_match.namespaces:
                # More than one namespace, really? Hmm.
                namespace = resolver_match.namespaces[0]
            resolved_view_name = ':%s:%s' % (namespace, resolver_match.url_name)
        except Resolver404:
            resolved_view_name = None

        self._cache_init()

        siteblocks_static = self._cache_get(block_alias)
        if not siteblocks_static:
            blocks = Block.objects.filter(alias=block_alias, hidden=False).only('url', 'contents')
            re_index = defaultdict(list)
            for block in blocks:
                if block.url == '*':
                    url_re = block.url
                elif block.url.startswith(':'):
                    url_re = block.url
                    # Normalize URL name to include namespace.
                    if url_re.count(':') == 1:
                        url_re = ':%s' % url_re
                else:
                    url_re = re.compile(r'%s' % block.url)
                re_index[url_re].append(block.contents)

            siteblocks_static = re_index
            self._cache_set(block_alias, re_index)
        self._cache_save()

        resulting_contents = ''
        if '*' in siteblocks_static:
            resulting_contents = choice(siteblocks_static['*'])
        elif resolved_view_name in siteblocks_static:
            resulting_contents = choice(siteblocks_static[resolved_view_name])
        else:
            for url, contents in siteblocks_static.items():
                if url.match(current_url):
                    resulting_contents = choice(contents)
                    break

        return resulting_contents


class SiteBlocksError(Exception):
    """Exception class for siteblocks application."""
    pass
