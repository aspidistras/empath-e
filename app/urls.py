from django.conf.urls import url

from app.views import user, base


app_name = 'app'

urlpatterns = [
    url(r'^$', base.index, name='index'),
    url(r'^legal-notices/$', base.legal_notices, name='legal_notices'),
    url(r'^resources/$', base.resources, name='resources'),
    url(r'^login/$', user.user_login, name="login"),
    url(r'^new-user/$', user.create_account, name="create_account"),
    url(r'^account/$', user.account, name="account"),
    url(r'^logout/$', user.user_logout, name='logout'),
]
