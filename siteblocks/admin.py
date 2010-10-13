from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib import messages

from models import Block

class BlockAdmin(admin.ModelAdmin):
    list_display = ('alias', 'description', 'url', 'hidden')
    search_fields = ['alias', 'url']
    list_filter = ['hidden']
    ordering = ['alias']
    
admin.site.register(Block, BlockAdmin)