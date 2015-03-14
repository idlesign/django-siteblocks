from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Block(models.Model):

    alias = models.CharField(
        _('Alias'), max_length=80, help_text=_('Short name to address this block from a template.'), db_index=True)
    description = models.CharField(
        _('Description'), max_length=100, help_text=_('Short memo for this block.'), null=True, blank=True)
    url = models.CharField(
        _('URL'), max_length=200,
        help_text=_('Page URL this block is related to. Regular expressions supported (e.g.: "/news.*" &#8212; '
                    'everything under "/news").<br />'
                    'View names are supported: prepend <b>:</b> to view name <br />'
                    '<b>Reserved URL alias:</b> "*" &#8212; every page.'))
    contents = models.TextField(
        _('Contents'), help_text=_('Block contents to render in a template.'))
    access_loggedin = models.BooleanField(
        _('Logged in only'),
        help_text=_('Check it to grant access to this block to authenticated users only.'),
        db_index=True, default=False)
    access_guest = models.BooleanField(
        _('Guests only'),
        help_text=_('Check it to grant access to this block to guests only.'), db_index=True, default=False)
    hidden = models.BooleanField(
        _('Hidden'), help_text=_('Whether to show this block when requested.'), db_index=True, default=False)
      
    class Meta(object):
        verbose_name = _('Site Block')
        verbose_name_plural = _('Site Blocks')
        
    def __str__(self):
        return self.alias
