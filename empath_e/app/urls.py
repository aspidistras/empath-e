from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('legal-notices', views.legal_notices, name='legal_notices')
]