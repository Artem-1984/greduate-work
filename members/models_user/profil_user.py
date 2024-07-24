from django.db import models
from django.conf import settings


class Setting_user(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=50)
    age = models.IntegerField()
    last_name = models.CharField(max_length=100)
    sity = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    floor = models.CharField(max_length=10)


class LikesUser(models.Model):
    user_like_prof = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    image_like = models.ForeignKey(Setting_user, on_delete=models.CASCADE)


class SmssUser(models.Model):
    sent_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    received_user = models.ForeignKey(Setting_user, on_delete=models.CASCADE)
    sms = models.CharField(max_length=500)
    data_sms = models.DateTimeField(auto_now_add=True)
    read_sms = models.BooleanField(default=False)
