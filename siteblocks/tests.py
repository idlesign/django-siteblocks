import unittest
from random import choice

from django import template, VERSION
from django.conf.urls import  url, include
from django.template import Template, Context

from siteblocks.models import Block
from siteblocks.siteblocksapp import SiteBlocks, register_dynamic_block

try:
    from django.conf.urls import patterns

except ImportError:
    patterns = None


class MockRequest(object):

    def __init__(self, path, user_authorized):
        self.path = path
        self.user = MockUser(user_authorized)


class MockUser(object):

    def __init__(self, authorized):
        self.authorized = authorized

    def is_authenticated(self):
        return self.authorized


def get_mock_patterns():
    url_ = url(r'^my_another_named_url/$', lambda r: None, name='url')

    if patterns:
        return patterns('', url_)

    return [url_]


class MockUrlconfModule(object):

    urlpatterns = get_mock_patterns()


urlpatterns = [
    url(r'^my_named_url/$', lambda r: None, name='named_url'),
    url(r'^namespace/', include((MockUrlconfModule, None, 'namespaced'))),
]

if VERSION < (1, 10):
    urlpatterns.insert(0, '')
    urlpatterns = patterns(*urlpatterns)


def get_mock_context(app=None, path=None, user_authorized=False):
    kwargs = {}

    if VERSION < (1, 10):
        kwargs['current_app'] = app

    ctx = template.Context({'request': MockRequest(path, user_authorized)}, **kwargs)
    return ctx


QUOTES = [  # From Terry Pratchett's Discworld novels.
    'Ripples of paradox spread out across the sea of causality.',
    'Early to rise, early to bed, makes a man healthy, wealthy and dead.',
    'Granny had nothing against fortune-telling provided it was done badly by people with no talent for it.',
    'Take it from me, there\'s nothing more terrible than someone out to do the world a favour.',
    'The duke had a mind that ticked like a clock and, like a clock, it regularly went cuckoo.',
    'Most gods find it hard to walk and think at the same time.',
    'They didn\'t have to be funny - they were father jokes',
    'Speak softly and employ a huge man with a crowbar.',
]


def get_quote(**kwargs):
    return choice(QUOTES)


class TemplateTagsTest(unittest.TestCase):

    def test_siteblock(self):
        context = Context()
        context['request'] = MockRequest('/', user_authorized=False)

        result = Template('{% load siteblocks %}{% siteblock "myblock" %}').render(context)
        self.assertEqual(result, '')

        b1 = Block(alias='myblock', url='*', contents='my_block_here')
        b1.save(force_insert=True)

        result = Template('{% load siteblocks %}{% siteblock "myblock" %}').render(context)
        self.assertEqual(result, 'my_block_here')

        Template('{% load siteblocks %}{% siteblock "myblock" as somevar %}').render(context)
        self.assertEqual(context.get('somevar'), 'my_block_here')


class TreeItemModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.siteblocks = SiteBlocks()

        cls.b1 = Block(alias='main', url='*', contents='main_every_visible')
        cls.b1.save(force_insert=True)

        cls.b2 = Block(alias='main', description='hidden', url='*', contents='main_every_hidden', hidden=True)
        cls.b2.save(force_insert=True)

        cls.b3 = Block(alias='multiple', url='*', contents='multiple_1')
        cls.b3.save(force_insert=True)

        cls.b4 = Block(alias='multiple', url='*', contents='multiple_2')
        cls.b4.save(force_insert=True)

        cls.b5 = Block(alias='filtered_1', url='/news.*', contents='filtered_1_1')
        cls.b5.save(force_insert=True)

        cls.b6 = Block(alias='filtered_1', url='/gro{1,2}ves', contents='filtered_1_2')
        cls.b6.save(force_insert=True)

        cls.b7 = Block(alias='named_1', url=':named_url', contents='named_1_1')
        cls.b7.save(force_insert=True)

        cls.b8 = Block(alias='named_2', url=':namespaced:url', contents='named_2_1')
        cls.b8.save(force_insert=True)

        cls.b9 = Block(alias='access_filter', url='*', contents='afilter_auth', access_loggedin=True)
        cls.b9.save(force_insert=True)

        cls.b10 = Block(alias='access_filter', url='*', contents='afilter_guest', access_guest=True)
        cls.b10.save(force_insert=True)

    def test_static_notalias(self):

        contents = self.siteblocks.get('notalias', get_mock_context(path='/root/'))
        self.assertEqual(contents, '')

    def test_static_asterisk(self):

        contents = self.siteblocks.get(self.b1.alias, get_mock_context(path='/root/'))
        self.assertEqual(contents, self.b1.contents)

        contents = self.siteblocks.get(self.b3.alias, get_mock_context(path='/root/'))
        self.assertIn(contents, [self.b3.contents, self.b4.contents])

    def test_static_multiple(self):

        contents = self.siteblocks.get(self.b5.alias, get_mock_context(path='/news/1'))
        self.assertEqual(contents, self.b5.contents)

        contents = self.siteblocks.get(self.b5.alias, get_mock_context(path='/news/2'))
        self.assertEqual(contents, self.b5.contents)

        contents = self.siteblocks.get(self.b5.alias, get_mock_context(path='/new/2'))
        self.assertEqual(contents, '')

    def test_static_regexp(self):

        contents = self.siteblocks.get(self.b5.alias, get_mock_context(path='/grooves'))
        self.assertEqual(contents, self.b6.contents)

        contents = self.siteblocks.get(self.b5.alias, get_mock_context(path='/groves'))
        self.assertEqual(contents, self.b6.contents)

        contents = self.siteblocks.get(self.b5.alias, get_mock_context(path='/groooves'))
        self.assertEqual(contents, '')

    def test_static_namedview(self):

        contents = self.siteblocks.get(self.b7.alias, get_mock_context(path='/my_named_url/'))
        self.assertEqual(contents, self.b7.contents)

        contents = self.siteblocks.get(self.b8.alias, get_mock_context(path='/namespace/my_another_named_url/'))
        self.assertEqual(contents, self.b8.contents)

    def test_dynamic(self):
        register_dynamic_block('quotes', get_quote)
        contents = self.siteblocks.get('quotes', get_mock_context(path='/somewhere/'))
        self.assertIn(contents, QUOTES)

    def test_static_access_filters(self):
        contents = self.siteblocks.get(self.b9.alias, get_mock_context(path='/some/'))
        self.assertEqual(contents, self.b10.contents)

        contents = self.siteblocks.get(self.b9.alias, get_mock_context(path='/some/', user_authorized=True))
        self.assertEqual(contents, self.b9.contents)
