from django.contrib import admin

# Register your models here.
from .models import Setting_user,BlodPost,Comment,SmssUser,Likes
# Register your models here.
@admin.register(Setting_user)
class BlodPostAdmin(admin.ModelAdmin):
    list_display = ('username','age')
    
@admin.register(BlodPost)
class BlodAdmin(admin.ModelAdmin):
    list_display = ('header','text')
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text','user_id')
    
@admin.register(SmssUser)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('sms','received_user','sent_user')
@admin.register(Likes)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('likes','user_like','blog_like')