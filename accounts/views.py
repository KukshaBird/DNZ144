from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import (LoginView, PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from django.contrib.auth.decorators import login_required

from . import forms

from . import models


class AccountDetailView(DetailView):
    # model = settings.AUTH_USER_MODEL
    model = models.ApiUser
    template_name = 'accounts/profile.html'


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        form.send_request()
        # form.create_profile(self.request)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


# def login_view(login):
# 	template_name = 'accounts/login.html'
# 	authentication_form = forms.UserLoginForm

class UserLoginView(LoginView):
    authentication_form = forms.UserLoginForm
    template_name = "accounts/login.html"


class ProfileUpdateView(UpdateView):
    form_class = forms.UserUpdateForm
    model = models.ApiUser
    template_name = 'accounts/update.html'

class UserPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("home")
    template_name = "accounts/reset_pass.html"
    email_template_name = "accounts/password_reset_email.html"

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/reset.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
