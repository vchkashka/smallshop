from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from .models import SellerReview
from django.shortcuts import redirect
from .forms import (LoginUserForm, RegisterUserForm, ProfileUserForm,
                    UserPasswordChangeForm, SellerReviewForm)
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings


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
    extra_context = {'title': "Профиль пользователя",
                     'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PublicProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'users/public_profile.html'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = SellerReview.objects.filter(
            seller=self.get_object())
        context['form'] = SellerReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = SellerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.seller = self.object
            review.save()
            return redirect('users:public_profile', pk=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
