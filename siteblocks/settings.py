from django.conf import settings


# Support for blocks dependent on get_language().
I18N_SUPPORT = getattr(settings, 'SITEBLOCKS_I18N_SUPPORT', False)
