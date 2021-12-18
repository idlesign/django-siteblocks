try:
    from django.urls import re_path, include

except ImportError:
    from django.conf.urls import url as re_path, include


urlpatterns = [
    re_path(r'^my_named_url/$', lambda r: None, name='named_url'),
]


def get_mock_patterns():
    return [re_path(r'^my_another_named_url/$', lambda r: None, name='url')]


class MockUrlconfModule:

    urlpatterns = get_mock_patterns()


urlpatterns.append(re_path(r'^namespace/', include((MockUrlconfModule, 'app'), namespace='namespaced')))
