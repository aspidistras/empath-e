from django.urls import path

from app.views import user, base


urlpatterns = [
    path('', base.index, name='index'),
    path('legal-notices/', base.legal_notices, name='legal_notices'),
    path('login/', user.user_login, name="login"),
]
