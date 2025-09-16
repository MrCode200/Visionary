from django.urls import path, include
from . import views
app_name = 'api'

urlpatterns = [
    path("send_msg/", views.recv_hijacked_msg),
    path("target/", views.send_target)
]