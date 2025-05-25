from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from .forms import (LoginUserForm, RegisterUserForm, ProfileUserForm,
                    UserPasswordChangeForm)
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return (self.request.POST.get('next')
                or self.request.GET.get('next')
                or reverse_lazy('home'))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


class PublicProfileView(DetailView):
    model = get_user_model()
    template_name = 'users/public_profile.html'
    context_object_name = 'seller'


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
