from django import template

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
    as_var = detect_clause(parser, 'as', tokens)
    tokens_num = len(tokens)

    if tokens_num in (2, 4):
        block_alias = parser.compile_filter(tokens[1])
        return siteblockNode(block_alias, as_var)    
    else:
        raise template.TemplateSyntaxError, "%r tag requires two or four arguments. E.g.: {%% siteblock \"myblock\" %%} or {%% siteblock \"myblock\" as myvar %%}." % tokens[0]


class siteblockNode(template.Node):

    def __init__(self, block_alias, as_var=None):
        self.block_alias = block_alias
        self.as_var = as_var
        
    def render(self, context):
        block_alias = self.block_alias
        if isinstance(self.block_alias, template.FilterExpression):
            block_alias = block_alias.resolve(context)

        contents = siteblocks.get(block_alias, context)

        if self.as_var is not None:
            context[self.as_var] = contents
            return ''

        return contents


def detect_clause(parser, clause_name, tokens):
    """Helper function detects a certain clause in tag tokens list.
    Returns its value.

    """
    if clause_name in tokens:
        t_index = tokens.index(clause_name)
        clause_value = parser.compile_filter(tokens[t_index + 1])
        del tokens[t_index:t_index + 2]
    else:
        clause_value = None
    return clause_value
