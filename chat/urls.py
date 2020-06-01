"""Chat urls"""


from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
    path('chat/<str:room_name>/', views.room, name='room'),
]
