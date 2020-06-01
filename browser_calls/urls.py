"""Browser calls related url patterns"""


from django.conf.urls import url
from .views import get_token, call


app_name = 'browser_calls'

urlpatterns = [
    url(r'^token/$', get_token, name='token'),
    url(r'^call/$', call, name='call'),
]
