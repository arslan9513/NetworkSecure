from django.urls import path
from .consumers import AlertConsumer

websocket_urlpatterns = [
    path('ws/duydurys/', AlertConsumer.as_asgi()),
]
