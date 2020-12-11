from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path


from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path('', GraphqlSubscriptionConsumer)
    ])),
})