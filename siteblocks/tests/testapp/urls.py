from django import VERSION
from django.conf.urls import url, include

try:
    from django.conf.urls import patterns

except ImportError:
    patterns = None


urlpatterns = [
    url(r'^my_named_url/$', lambda r: None, name='named_url'),
]


def get_mock_patterns():
    url_ = url(r'^my_another_named_url/$', lambda r: None, name='url')

    if patterns:
        return patterns('', url_)

    return [url_]


class MockUrlconfModule(object):

    urlpatterns = get_mock_patterns()


if VERSION < (2, 0):
    urlpatterns.append(url(r'^namespace/', include((MockUrlconfModule, None, 'namespaced'))))
else:
    urlpatterns.append(url(r'^namespace/', include((MockUrlconfModule, 'app'), namespace='namespaced')))


if VERSION < (1, 10):
    urlpatterns.insert(0, '')
    urlpatterns = patterns(*urlpatterns)
