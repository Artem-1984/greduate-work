from django import forms
from django.forms import ModelForm

from .models import *
import django_filters
from django_filters import rest_framework as filters

class SettingForm(forms.ModelForm):

    class Meta:
        model = Setting_user
        fields = ('user','username','last_name',"image",'age','sity','about','floor')


class ProfileFilter(django_filters.FilterSet):
    min_age = filters.NumberFilter(field_name='age', lookup_expr='gte')
    max_age = filters.NumberFilter(field_name='age', lookup_expr='lte')
    class Meta:
        model = Setting_user
        fields = ['username','sity','floor','age']
class BlodPostForm(forms.ModelForm):
    class Meta:
        model = BlodPost
        fields = ('header','text','user')
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text','user_comments','user')
class LikesForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = ('likes','user_like','blog_like')
class SmsForm(forms.ModelForm):
    class Meta:
        model = SmssUser
        fields = ('sms','sent_user','received_user')
        
class LikesUserForm(forms.ModelForm):
    class Meta:
        model = LikesUser
        fields = ('user_like_prof','likes','image_like')

        
        
