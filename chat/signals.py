# signals.py
from django.db.models.signals import pre_save , post_delete
from graphene_subscriptions.signals import pre_save_subscription, post_delete_subscription

from chat.models import Message

pre_save.connect(pre_save_subscription, sender=Message, dispatch_uid="message_pre_save")
post_delete.connect(post_delete_subscription, sender=Message, dispatch_uid="message_post_delete")
