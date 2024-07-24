from django.contrib.auth.models import User
from .models import Setting_user, BlodPost, Comment, Likes, SmssUser, LikesUser
import os

def all_users():
    """Вывод пользователей по дате"""
    users = Setting_user.objects.order_by('-user_id')
    return users


def search_user(search_username: str, search_floor: str, search_age1: str, search_age2: str, search_city: str):
    '''Вывод определенного пользователя по параметрам'''
    sorting_user = (Setting_user.objects.filter(username=search_username) | Setting_user.objects.filter(
        floor=search_floor) | Setting_user.objects.filter(sity=search_city)) & Setting_user.objects.filter(
        age__range=(search_age1, search_age2))
    return sorting_user


def registration(username: str, email: str, password: str):
    '''Регистрация пользователя на сайте'''
    User.objects.create_user(username, email, password)


def user_like(pk):
    """Получение количества лайков пользователя"""
    like = len(LikesUser.objects.filter(image_like=pk))
    return like


def changes_like(sender_user: str, recipient_user: str, form: str):
    '''Добавление и удаление лайков'''
    changes = LikesUser.objects.filter(user_like_prof=sender_user) & LikesUser.objects.filter(image_like=recipient_user)
    if changes:
        changes.delete()
    else:
        form.save()


def article():
    """Вывод всех статей"""
    all_article = BlodPost.objects.order_by('-date')
    return all_article


def del_acticle(delit: str):
    """Удаление статьи"""
    user_acticle = BlodPost.objects.get(id=delit)
    user_acticle.delete()


def sort_acticle(request, radio_btn: str, text_btn: str):
    """Сортировка статей"""
    print(radio_btn)
    if radio_btn == 'new':
        sort_article = BlodPost.objects.order_by('-date')
    elif radio_btn == 'your_entries':
        sort_article = BlodPost.objects.filter(user=request.user.id)
    else:
        sort_article = BlodPost.objects.filter(header=text_btn.upper())
    return sort_article


def acticle_like(pk):
    """Отображение количества лайков в статьях"""
    acticle_like = (len(Likes.objects.filter(blog_like=pk)))
    print(acticle_like)
    return acticle_like


def acticle_like_users(pk):
    """Отображение пользователей кто поставил лайк"""
    acticle_like_users = (Likes.objects.filter(blog_like=pk))
    return acticle_like_users



def del_comment(delit: str):
    """Удаление комментарий"""
    all_comment = Comment.objects.all()
    search_comment_del = Comment.objects.get(id=delit)
    search_comment_del.delete()


def likes_change_arcticle(form: str):
    '''Изменение лайков пользователя'''
    like_arcticle = form.cleaned_data['blog_like']
    like_user = form.cleaned_data['user_like']
    change_like = Likes.objects.filter(user_like=like_user) & Likes.objects.filter(blog_like=like_arcticle)
    if change_like:
        change_like.delete()
    else:
        form.save()


def mesage_user(request):
    """Отображение чатов пользователя"""

    all_user = Setting_user.objects.all()
    list_communication_user = []
    for i in all_user:
        search_communication_user = ((SmssUser.objects.filter(received_user=i.user_id) & SmssUser.objects.filter(
            sent_user=request.user.id) | SmssUser.objects.filter(sent_user=i.user_id) & SmssUser.objects.filter(
            received_user=request.user.id)).last())
        if search_communication_user == None:
            continue
        list_communication_user.append(search_communication_user)
    list_communication_user.sort(key=lambda x: x.id, reverse=True)
    return list_communication_user


def read_mesage_user(request, user_mesage: str):
    """Отображение непрочитанных сообщений"""
    list_unread = []
    for i in user_mesage:
        if i.sent_user.id != request.user.id:
            if i.read_sms == False:
                list_unread.append(i)
    return list_unread


def chat_user(request, one_chat: str):
    '''чат с конкретным пользователем '''
    search_chat_user = (SmssUser.objects.filter(received_user=one_chat.id) & SmssUser.objects.filter
    (sent_user=request.user.id)) | (SmssUser.objects.filter
                                    (received_user=request.user.id) & SmssUser.objects.filter
                                    (sent_user=one_chat.user.id)).order_by('-data_sms')
    return search_chat_user


def read_sms(request, one_chat: str):
    '''при переходе в чат, сообщения прочитываются '''
    read_chat_user = (SmssUser.objects.filter(received_user=request.user.id) & SmssUser.objects.filter(
        sent_user=one_chat.user.id))
    for i in read_chat_user:
        if i.read_sms == False:
            i.read_sms = True
            i.save()


def del_sms(delit: str):
    '''удаление сообщения в чате'''
    sms = SmssUser.objects.get(id=delit)
    sms.delete()


def change_image(request, user_prof: str, image_text):
    '''Изменение фотографии пользователя'''
    if len(request.FILES) != 0:
        if len(user_prof.image) > 0:
            os.remove(user_prof.image.path)
        user_prof.image = image_text
        user_prof.save()


def change_profile(request, username_text: str, age_text: str, last_name_text: str, sity_text: str, about_text: str,
                   floor_text: str):
    '''Изменения данных пользователя'''
    Setting_user.objects.filter(id=request.user.id).update(username=username_text,
                                                           age=age_text,
                                                           last_name=last_name_text,
                                                           sity=sity_text,
                                                           about=about_text,
                                                           floor=floor_text,
                                                           )


def search_login_user(username: str, mail: str):
    '''Поиск аккаунта пользователя'''
    user = User.objects.get(username=username, email=mail)
    return user


def change_login_user(user: str, passwords: str):
    '''Изменение пароля пользователя'''
    user.set_password(passwords)
    user.save()
