from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import *
from .templates_name import *
from .exceptions import ValueError,DoesNotExist

class Home(View):
    def get(self, request):
        '''Страница со всеми пользователями и сортировка по их данным'''
        users = ProfileFilter(request.GET, queryset=Setting_user.objects.order_by('-user_id'))
        return render(request, home_page, {'users': users})


class Register(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        """Регистрация новых пользователей"""
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password2 == password:
                user_register = registration(username=username, email=email,
                                             password=password)
                return redirect('/')
            else:
                context = {
                    "error": "Логин или пароль неправильные"
                }
                return render(request, registration_page, context)

        return render(request, registration_page)


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        """Выход из аккаунта"""
        logout(request)
        return redirect('/')


class Settting(View):
    def get(self, request):
        """Страница настроек пользователя"""
        return render(request, setting_page)

    def post(self, request, *args, **kwargs):
        """Авторизация и аутификация"""
        if 'entrance' in self.request.POST:

            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is None:
                    context = {
                        "error": "Логин или пароль неправильные"
                    }
                    return render(request, setting_page, context)
                login(request, user)
                return redirect(setting_redirect_page)
        else:
            """Добавление данных пользователя"""
            form_user_data = SettingForm(request.POST, request.FILES)
            user_data = Setting_user.objects.filter(id=request.user.id)
            if form_user_data.is_valid():
                form_user_data.save()
                img_obj = form_user_data.instance
                return render(request, setting_page, {'form_user_data': form_user_data, 'img_obj': img_obj})
            else:
                raise ValueError
            return render(request, setting_page, {'form_user_data': form_user_data})


class Red(LoginRequiredMixin, View):
    def get(self, request, pk):
        """Страница пользователя"""
        user_data = Setting_user.objects.get(id=pk)
        like = user_like(pk=pk)
        return render(request, user_profile, {'user_data': user_data, 'like': like})

    def post(self, request, pk):
        """Лайки пользователям"""
        user_data = Setting_user.objects.get(id=pk)
        form = LikesUserForm(request.POST)
        if form.is_valid():
            recipient_user = form.cleaned_data['image_like']
            sender_user = form.cleaned_data['user_like_prof']
            like_user = changes_like(recipient_user=recipient_user, sender_user=sender_user, form=form)
        like = user_like(pk=pk)
        return render(request, user_profile, {'user_data': user_data, 'like': like})


class Blog(LoginRequiredMixin, View):
    def get(self, request):
        """"Страница со всеми статьями блога"""
        all = article()
        return render(request, article_page, {'all': all})

    def post(self, request):
        if 'garbage' in self.request.POST:
            """ Удаление статей"""
            all_article = article()
            delit = request.POST.get('garbage', None)
            delit_acticle = del_acticle(delit=delit)
            return render(request, article_page, {'all': all_article})
        elif 'search' in self.request.POST:
            """ Сортировка статей"""
            radio_btn = request.POST.get('new')
            text_btn = request.POST.get('text_search', None)
            sort_article = sort_acticle(request, radio_btn=radio_btn, text_btn=text_btn)
            return render(request, article_page, {'all': sort_article})


class PostBlog(LoginRequiredMixin, View, PermissionRequiredMixin):
    def get(self, request, pk):
        """Отображения отдельной статьи блога """
        one_acticle = BlodPost.objects.get(id=pk)
        user_like = acticle_like_users(pk=pk)
        acticle_likes = acticle_like(pk=pk)
        return render(request, article_users_page,
                      {'one_acticle': one_acticle, 'user_like': user_like, 'acticle_likes': acticle_likes})

    def post(self, request, pk):
        if 'garbage' in self.request.POST:
            """Удаление комментариев """
            one_acticle = BlodPost.objects.get(id=pk)
            user_like = acticle_like_users(pk=pk)
            acticle_likes = acticle_like(pk=pk)
            delit = request.POST.get('garbage', None)
            del_comments = del_comment(delit=delit)
            return render(request, article_users_page,
                          {'one_acticle': one_acticle, 'user_like': user_like, 'acticle_likes': acticle_likes})
        elif 'likes' in self.request.POST:
            """Лайки статьям"""
            one_acticle = BlodPost.objects.get(id=pk)
            form = LikesForm(request.POST)
            if form.is_valid():
                change = likes_change_arcticle(form=form)
            user_like = acticle_like_users(pk=pk)
            acticle_likes = acticle_like(pk=pk)
            return render(request, article_users_page,
                          {'one_acticle': one_acticle, 'user_like': user_like, 'acticle_likes': acticle_likes})
        else:
            """Добавление комментариев """
            form = CommentForm(request.POST)
            one_acticle = BlodPost.objects.get(id=pk)
            user_like = acticle_like_users(pk=pk)
            acticle_likes = acticle_like(pk=pk)
            if form.is_valid():
                form.save()
                return render(request, article_users_page,
                              {'one_acticle': one_acticle, 'user_like': user_like, 'acticle_likes': acticle_likes})
            else:
                form = CommentForm()
                one_acticle = BlodPost.objects.get(id=pk)

            return render(request, article_users_page,
                          {'one_acticle': one_acticle, 'user_like': user_like, 'acticle_likes': acticle_likes})


class Message(LoginRequiredMixin, View):
    def get(self, request, pk):
        """Отображение чатов пользователя"""
        user_mesage = mesage_user(request)
        one_chat = Setting_user.objects.get(id=pk)
        read_user = read_mesage_user(request, user_mesage=user_mesage)
        return render(request, message_page, {'user_mesage': user_mesage, 'read_user': read_user})


class MessageSms(LoginRequiredMixin, View):
    def get(self, request, pk):
        """Чат с определенным пользователем"""
        one_chat = Setting_user.objects.get(id=pk)
        chat = chat_user(request, one_chat=one_chat)
        read = read_sms(request, one_chat=one_chat)
        return render(request, chat_page, {'one_chat': one_chat, 'chat': chat})

    def post(self, request, pk):
        if 'del' in self.request.POST:
            """Удаление смс"""
            one_chat = Setting_user.objects.get(id=pk)
            delit = request.POST.get('id', None)
            chat = chat_user(request, one_chat=one_chat)
            delit_sms = del_sms(delit=delit)
            return render(request, chat_page, {'one_chat': one_chat, 'chat': chat})
        else:
            """Добавление смс"""
            form = SmsForm(request.POST)
            if form.is_valid():
                one_chat = Setting_user.objects.get(id=pk)
                chat = chat_user(request, one_chat=one_chat)
                form.save()
            else:
                raise ValueError
            return render(request, chat_page, {'one_chat': one_chat, 'chat': chat})


class UserLike(LoginRequiredMixin, View):
    def get(self, request, pk):
        """Добавление лойков пользователям"""
        post = LikesUser.objects.filter(image_like=pk)
        return render(request, user_like_page, {'post': post})


class Change(LoginRequiredMixin, View):
    def get(self, request, pk):
        """Изменение профиля пользователя"""
        user_prof = Setting_user.objects.get(user_id=pk)
        return render(request, change_page, {'user_prof': user_prof})

    def post(self, request, pk):
        """Сохранение изменений профиля пользователя"""
        user_prof = Setting_user.objects.get(user_id=pk)
        username_text = request.POST.get('username')
        age_text = request.POST.get('age')
        last_name_text = request.POST.get('last_name')
        sity_text = request.POST.get('sity')
        about_text = request.POST.get('about')
        floor_text = request.POST.get('floor')
        image_text = request.FILES.get('image', None)
        image = change_image(request, image_text=image_text, user_prof=user_prof)
        change_prof = change_profile(request, username_text=username_text, age_text=age_text,
                                     last_name_text=last_name_text, sity_text=sity_text,
                                     about_text=about_text, floor_text=floor_text)
        return redirect(change_redirect)


class Add(LoginRequiredMixin, View):
    def get(self, request, pk):
        """Отображения страницы с добавлением статей"""
        post = Setting_user.objects.get(id=pk)
        return render(request, add_blog, {'post': post})

    def post(self, request, pk):
        """Сохранение статьи"""
        form = BlodPostForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = BlodPostForm()
        return redirect(article_redirect)


class Replay(View):
    def get(self, request):
        """Отображение страницы смены пароля"""
        return render(request, replay_page)

    def post(self, request, *args, **kwargs):
        """Смена пароля"""
        if request.method == 'POST':
            username = request.POST.get('username')
            passwords = request.POST.get('password')
            password2 = request.POST.get('password2')
            mail = request.POST.get('email')
            if passwords == password2:
                search_user = search_login_user(username=username, mail=mail)
                if search_user is None:
                    context = {
                        "error": "Логин или пароль неправильные"
                    }
                    return render(request, replay_page, context)
                else:
                    change_password = change_login_user(user=search_user, passwords=passwords)
                    return redirect('/')
            else:
                context = {
                    "error": "Логин или пароль неправильные"
                }
                return render(request, replay_page, context)
        return render(request, replay_page)
