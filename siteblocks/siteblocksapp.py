import re
from collections import defaultdict
from random import choice
from typing import Callable, Dict, List

from django.core.cache import cache
from django.db.models import signals
from django.template import Context
from django.urls import resolve, Resolver404
from django.utils.translation import get_language

from .models import Block
from .settings import I18N_SUPPORT

if I18N_SUPPORT:

    def cache_get_key(block_alias: str) -> str:
        return f'{block_alias}:{get_language()}'

else:
    def cache_get_key(block_alias: str) -> str:
        return block_alias


# Contains dynamic blocks.
_DYNAMIC_BLOCKS = defaultdict(list)


def register_dynamic_block(alias: str, callable: Callable):
    """Registers a callable that produces contents for a dynamic block.

    Callable on call will get the following kwargs:

        * `block_alias` - block alias,
        * `block_context` - template context for block

    Example::

        # Put the following code somewhere where it'd be triggered as expected. E.g. in app view.py.

        from random import choice
        # Import the register function.
        from siteblocks.siteblocksapp import register_dynamic_block


        # The following function will be used as a block contents producer.
        def get_quote(**kwargs):
            quotes = [  # From Terry Pratchett's Discworld novels.
                'Ripples of paradox spread out across the sea of causality.',
                'Early to rise, early to bed, makes a man healthy, wealthy and dead.',
                'Granny had nothing against fortune-telling provided it was done badly by people with no talent for it.'
                'Take it from me, there\'s nothing more terrible than someone out to do the world a favour.',
                'The duke had a mind that ticked like a clock and, like a clock, it regularly went cuckoo.',
                'Most gods find it hard to walk and think at the same time.',
                'They didn\'t have to be funny - they were father jokes',
                'Speak softly and employ a huge man with a crowbar.',
            ]
            return choice(quotes)

        # And we register our siteblock.
        register_dynamic_block('quote', get_quote)

    """
    global _DYNAMIC_BLOCKS
    _DYNAMIC_BLOCKS[alias].append(callable)


def get_dynamic_blocks() -> Dict[str, List[Callable]]:
    """Returns a dictionary with currently registered dynamic blocks."""
    return _DYNAMIC_BLOCKS


class SiteBlocks:

    # siteblocks objects are stored in Django cache for a year (60 * 60 * 24 * 365 = 31536000 sec).
    # Cache is only invalidated on block item change.
    CACHE_TIMEOUT: str = 31536000
    CACHE_KEY: str = 'siteblocks'

    IDX_GUEST: int = 0
    IDX_AUTH: int = 1

    def __init__(self):
        self._cache = None
        signals.post_save.connect(self._cache_empty, sender=Block)
        signals.post_delete.connect(self._cache_empty, sender=Block)

    def _cache_init(self):
        """Initializes local cache from Django cache."""
        cache_ = cache.get(self.CACHE_KEY)
        if cache_ is None:
            cache_ = defaultdict(dict)
        self._cache = cache_

    def _cache_save(self):
        cache.set(self.CACHE_KEY, self._cache, self.CACHE_TIMEOUT)

    def _cache_get(self, key: str) -> List[Dict[str, List]]:
        """Returns cache entry parameter value by its name."""
        return self._cache.get(key, False)

    def _cache_set(self, key: str, value: List[Dict[str, List]]):
        """Replaces entire cache entry parameter data by its name with new data."""
        self._cache[key] = value

    def _cache_empty(self, **kwargs):
        self._cache = None
        cache.delete(self.CACHE_KEY)

    def get_contents_static(self, block_alias: str, context: Context) -> str:
        """Returns contents of a static block."""

        if 'request' not in context:
            # No use in further actions as we won't ever know current URL.
            return ''

        current_url = context['request'].path

        # Resolve current view name to support view names as block URLs.
        try:
            resolver_match = resolve(current_url)
            namespace = ''

            if resolver_match.namespaces:
                # More than one namespace, really? Hmm.
                namespace = resolver_match.namespaces[0]

            resolved_view_name = f':{namespace}:{resolver_match.url_name}'

        except Resolver404:
            resolved_view_name = None

        self._cache_init()

        cache_entry_name = cache_get_key(block_alias)
        idx_guest = self.IDX_GUEST
        idx_auth = self.IDX_AUTH

        siteblocks_static = self._cache_get(cache_entry_name)

        if not siteblocks_static:

            blocks = Block.objects.filter(
                alias=block_alias,
                hidden=False
            ).only('url', 'contents', 'access_guest', 'access_loggedin')

            siteblocks_static = [defaultdict(list), defaultdict(list)]

            for block in blocks:

                if block.url == '*':
                    url_re = block.url

                elif block.url.startswith(':'):
                    url_re = block.url
                    # Normalize URL name to include namespace.
                    if url_re.count(':') == 1:
                        url_re = f':{url_re}'

                else:
                    url_re = re.compile(rf'{block.url}')

                if block.access_guest:
                    siteblocks_static[idx_guest][url_re].append(block.contents)

                elif block.access_loggedin:
                    siteblocks_static[idx_auth][url_re].append(block.contents)

                else:
                    siteblocks_static[idx_guest][url_re].append(block.contents)
                    siteblocks_static[idx_auth][url_re].append(block.contents)

            self._cache_set(cache_entry_name, siteblocks_static)

        self._cache_save()

        user = getattr(context['request'], 'user', None)
        is_authenticated = getattr(user, 'is_authenticated', False)

        lookup_area = siteblocks_static[idx_auth if is_authenticated else idx_guest]

        static_block_contents = ''

        if '*' in lookup_area:
            static_block_contents = choice(lookup_area['*'])

        elif resolved_view_name in lookup_area:
            static_block_contents = choice(lookup_area[resolved_view_name])

        else:
            for url, contents in lookup_area.items():
                if url.match(current_url):
                    static_block_contents = choice(contents)
                    break

        return static_block_contents

    def get_contents_dynamic(self, block_alias: str, context: Context) -> str:
        """Returns contents of a dynamic block."""
        dynamic_block = get_dynamic_blocks().get(block_alias, [])

        if not dynamic_block:
            return ''

        dynamic_block = choice(dynamic_block)
        return dynamic_block(block_alias=block_alias, block_context=context)

    def get(self, block_alias: str, context: Context) -> str:
        """Main method returning block contents (static or dynamic)."""
        contents = []

        dynamic_block_contents = self.get_contents_dynamic(block_alias, context)
        if dynamic_block_contents:
            contents.append(dynamic_block_contents)

        static_block_contents = self.get_contents_static(block_alias, context)
        if static_block_contents:
            contents.append(static_block_contents)

        if not contents:
            return ''

        return choice(contents)
