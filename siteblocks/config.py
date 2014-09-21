from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SiteblocksConfig(AppConfig):
    """Siteblocks configuration."""

    name = 'siteblocks'
    verbose_name = _('Site Blocks')
