from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Block


class BlockAdmin(admin.ModelAdmin):

    list_display = ('alias', 'description', 'url', 'hidden', 'access_loggedin', 'access_guest')
    search_fields = ['alias', 'url']
    list_filter = ['hidden']
    ordering = ['alias']
    fieldsets = (
        (_('Basic settings'), {
            'fields': ('alias', 'url', 'contents',)
        }),
        (_('Access settings'), {
            'classes': ('collapse',),
            'fields': ('access_loggedin', 'access_guest')
        }),
        (_('Additional settings'), {
            'fields': ('description', 'hidden')
        }),
    )


admin.site.register(Block, BlockAdmin)
