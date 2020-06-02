"""Chat urls"""


from django.conf.urls import url

from . import views

app_name = "chat"

urlpatterns = [
    url(r'^(?P<room_name>[^/]+)/$', views.room, name="room"),
]

