from django.db import models
from .profil_user import Setting_user

class BlodPost(models.Model):
    header = models.CharField('Заголовок', max_length=30)
    text = models.TextField('Содержание', max_length=100000)
    date = models.DateTimeField('Дата', auto_now_add=True)
    user = models.ForeignKey(Setting_user, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=500)
    date_comment = models.DateTimeField(auto_now_add=True)
    user_comments = models.ForeignKey(Setting_user, on_delete=models.CASCADE)
    user = models.ForeignKey(BlodPost, on_delete=models.CASCADE)


class Likes(models.Model):
    user_like = models.ForeignKey(Setting_user, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    blog_like = models.ForeignKey(BlodPost, on_delete=models.CASCADE)