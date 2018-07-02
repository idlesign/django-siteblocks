from random import choice

from siteblocks.models import Block
from siteblocks.siteblocksapp import SiteBlocks, register_dynamic_block


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


class TestTemplateTags(object):

    def test_siteblock(self, template_render_tag, template_context):

        context = template_context({})

        assert template_render_tag('siteblocks', 'siteblock "myblock"', context) == ''

        b1 = Block(alias='myblock', url='*', contents='my_block_here')
        b1.save(force_insert=True)

        assert template_render_tag('siteblocks', 'siteblock "myblock"', context) == 'my_block_here'

        template_render_tag('siteblocks', 'siteblock "myblock" as somevar', context)
        assert context.get('somevar') == 'my_block_here'


class TestTreeItemModel(object):

    @classmethod
    def setup_method(cls):
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

    def test_static_notalias(self, template_context):

        contents = self.siteblocks.get('notalias', template_context({}, '/root/'))
        assert contents == ''

    def test_static_asterisk(self, template_context):

        contents = self.siteblocks.get(self.b1.alias, template_context({}, '/root/'))
        assert contents == self.b1.contents

        contents = self.siteblocks.get(self.b3.alias, template_context({}, '/root/'))
        assert contents in [self.b3.contents, self.b4.contents]

    def test_static_multiple(self, template_context):

        contents = self.siteblocks.get(self.b5.alias, template_context({}, '/news/1'))
        assert contents == self.b5.contents

        contents = self.siteblocks.get(self.b5.alias, template_context({}, '/news/2'))
        assert contents == self.b5.contents

        contents = self.siteblocks.get(self.b5.alias, template_context({}, '/new/2'))
        assert contents == ''

    def test_static_regexp(self, template_context):

        contents = self.siteblocks.get(self.b5.alias, template_context({}, '/grooves'))
        assert contents == self.b6.contents

        contents = self.siteblocks.get(self.b5.alias, template_context({}, '/groves'))
        assert contents == self.b6.contents

        contents = self.siteblocks.get(self.b5.alias, template_context({}, '/groooves'))
        assert contents == ''

    def test_static_namedview(self, template_context):

        contents = self.siteblocks.get(self.b7.alias, template_context({}, '/my_named_url/'))
        assert contents == self.b7.contents

        contents = self.siteblocks.get(self.b8.alias, template_context({}, '/namespace/my_another_named_url/'))
        assert contents == self.b8.contents

    def test_dynamic(self, template_context):
        register_dynamic_block('quotes', get_quote)
        contents = self.siteblocks.get('quotes', template_context({}, '/somewhere/'))
        assert contents in QUOTES

    def test_static_access_filters(self, template_context, user_create):
        contents = self.siteblocks.get(self.b9.alias, template_context({}, '/some/'))
        assert contents == self.b10.contents

        contents = self.siteblocks.get(self.b9.alias, template_context({}, '/some/', user=user_create()))
        assert contents == self.b9.contents
