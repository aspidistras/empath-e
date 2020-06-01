"""App urls pattern"""

from django.conf.urls import url

from app.views import user, base


app_name = 'app'

urlpatterns = [
    url(r'^$', base.index, name='index'),
    url(r'^legal-notices/$', base.legal_notices, name='legal_notices'),
    url(r'^resources/$', base.resources, name='resources'),
    url(r'^login/$', user.user_login, name="login"),
    url(r'^new-user/(?P<group>[A-z]+)$', user.create_account, name="create_account"),
    url(r'^new-user/$', user.create_account, name="create_account"),
    url(r'^account/$', user.account, name="account"),
    url(r'^rules/$', user.rules, name='rules'),
    url(r'^logout/$', user.user_logout, name='logout'),
    url(r'^testimonies/$', base.testimonies, name='testimonies'),
    url(r'^about/$', base.about, name='about'),
    url(r'^disorders/$', base.disorders_list, name='disorders_list'),
    url(r'^disorder/(?P<disorder_name>[a-z]+)/$', base.disorder_details, name='disorder_details'),
    url(r'^request/$', user.new_request, name='request'),
    url(r'^testify/$', user.new_testimony, name="testify"),
    url(r'^requests-list/$', user.requests_list, name="requests_list"),
    url(r'^delete/$', user.delete_account, name="delete_account"),
    url(r'^request-info/(?P<request_id>[0-9]+)/$', user.request_info, name="request_info"),
    url(r'^accept-request/(?P<request_id>[0-9]+)/$', user.accept_request, name="accept_request"),
    url(r'^my-requests/$', user.user_requests_list, name="user_requests_list"),
    url(r'^archive-request/(?P<request_id>[0-9]+)/$', user.archive_request, name="archive_request"),
]
