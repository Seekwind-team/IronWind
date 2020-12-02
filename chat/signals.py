# signals.py
from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from chat.models import Message

post_save.connect(post_save_subscription, sender=Message, dispatch_uid="message_post_save")
post_delete.connect(post_delete_subscription, sender=Message, dispatch_uid="message_post_delete")
