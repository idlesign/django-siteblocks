from django import template
from django.template.base import FilterExpression

from ..siteblocksapp import SiteBlocks

register = template.Library()

# Utility methods are implemented in SiteBlocks class
siteblocks = SiteBlocks()


@register.tag
def siteblock(parser, token):
    """Two notation types are acceptable:

        1. Two arguments:
           {% siteblock "myblock" %}
           Used to render "myblock" site block.
           
        2. Four arguments:
           {% siteblock "myblock" as myvar %}
           Used to put "myblock" site block into "myvar" template variable.
           
    """
    tokens = token.split_contents()
    tokens_num = len(tokens)

    if tokens_num not in (2, 4):
        raise template.TemplateSyntaxError(
            '%r tag requires two or four arguments. '
            'E.g.: {%% siteblock "myblock" %%} or {%% siteblock "myblock" as myvar %%}.' % tokens[0])

    block_alias = parser.compile_filter(tokens[1])
    as_var = None
    tokens = tokens[2:]
    if len(tokens) >= 2 and tokens[-2] == 'as':
        as_var = tokens[-1]

    return siteblockNode(block_alias, as_var)


class siteblockNode(template.Node):

    def __init__(self, block_alias, as_var=None):
        self.block_alias = block_alias
        self.as_var = as_var
        
    def render(self, context):
        block_alias = self.block_alias
        if isinstance(self.block_alias, FilterExpression):
            block_alias = block_alias.resolve(context)

        contents = siteblocks.get(block_alias, context)

        if self.as_var is not None:
            context[self.as_var] = contents
            return ''

        return contents
