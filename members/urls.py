from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view()),

    path('<int:pk>/', views.Red.as_view(), name='red'),
    path('register', views.Register.as_view(), name='register '),
    path('settings_user', views.Settting.as_view(), name='settings_user'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('bloger', views.Blog.as_view(), name='blog'),
    path('cm/<int:pk>/', views.PostBlog.as_view(), name='blog'),
    path('message/<int:pk>/', views.Message.as_view(), name='message'),
    path('sms/<int:pk>/', views.MessageSms.as_view(), name='text'),
    path('<int:pk>/user_like', views.UserLike.as_view(), name='user_like'),
    path('change/<int:pk>/', views.Change.as_view(), name='change'),
    path('addblog/<int:pk>/', views.Add.as_view(), name='addblog'),
    path('replay', views.Replay.as_view(), name='replay'),


]
