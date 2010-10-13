import re

from django import template
from django.db.models import signals

from ..models import Block

register = template.Library()

class BlocksCache():
    
    def __init__(self):
        self.cache_blocks = {}
        signals.post_save.connect(self.cache_empty, sender=Block)
        signals.post_delete.connect(self.cache_empty, sender=Block)
        
    def cache_empty(self, **kwargs):
        self.cache_blocks = {}
        
mycache = BlocksCache()

@register.tag
def siteblock(parser, token):
    """Parses siteblock tag parameters.
    
    Two notation types are possible:
        1. Two arguments:
           {% siteblock "myblock" %}
           Used to render "myblock" site block.
           
        2. Four arguments:
           {% siteblock "myblock" as myvar %}
           Used to render "myblock" site block into variable "myvar".
           
    """
    tokens = token.split_contents()
    
    as_var = None
    if 'as' in tokens:
        tindex = tokens.index('as')
        as_var = tokens[tindex+1]
        del tokens [tindex:tindex+2]

    tokensNum = len(tokens)

    if tokensNum == 2:
        block_alias = tokens[1][1:-1].strip()
        return siteblockNode(block_alias, as_var)    
    else:
        raise template.TemplateSyntaxError, "%r tag requires two or four arguments. E.g.: {%% siteblock \"myblock\" %%} or {%% siteblock \"myblock\" as myvar %%}." % tokens[0]

class siteblockNode(template.Node):
    """Renders specified site block."""
    def __init__(self, block_alias, as_var=None):
        self.block_alias = block_alias
        self.as_var = as_var
        
    def render(self, context):
        
        block_alias = self.block_alias
        if block_alias.find(' ') == -1:
            try:
                block_alias = template.Variable(block_alias).resolve(context) 
            except template.VariableDoesNotExist:
                pass

        if 'request' in context:
            current_url = context['request'].path
        else:
            current_url = ''
            
        contents = ''
        
        if block_alias not in mycache.cache_blocks: 
            mycache.cache_blocks[block_alias] = {}
            blocks = Block.objects.filter(alias=block_alias, hidden=False).only('url', 'contents')
            for block in blocks:
                if block.url != '*':
                    url_re = re.compile(r'%s' % block.url)
                else:
                    url_re = block.url
                mycache.cache_blocks[block_alias][url_re] = block.contents

        if mycache.cache_blocks[block_alias].has_key('*'):
            contents = mycache.cache_blocks[block_alias]['*']
        else:
            for url in mycache.cache_blocks[block_alias]:
                if url.match(current_url):
                    contents = mycache.cache_blocks[block_alias][url]
                    break
        
        if self.as_var is not None:
            context[self.as_var] = contents
            return ''
        else:
            return contents
