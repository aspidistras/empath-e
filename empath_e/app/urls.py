from django.conf.urls import url

from app.views import user, base


app_name = 'app'

urlpatterns = [
    url(r'^$', base.index, name='index'),
    url(r'^legal-notices/$', base.legal_notices, name='legal_notices'),
    url(r'^login/$', user.user_login, name="login"),
    url(r'^new-user/$', user.create_account, name="create_account"),
]
