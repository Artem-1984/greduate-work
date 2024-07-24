from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import SmssUser
from django.core.signals import request_started





# @receiver(request_started)
# def post_save_sms(**kwargs):
#     print("Новое сообщение")