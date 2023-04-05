from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import RedirectURLMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import (LoginForm, PasswordChangeForm, PasswordCheckForm,
                         UserCreationForm)


class SignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')


class LoginView(RedirectURLMixin, FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    next_page = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class PasswordCheckView(LoginRequiredMixin, FormView):
    template_name = 'users/check_password.html'
    form_class = PasswordCheckForm
    success_url = reverse_lazy('users:change_password')

    def get_form_kwargs(self):
        ctx = super().get_form_kwargs()
        ctx['instance'] = self.request.user
        return ctx

    def form_valid(self, form):
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'users/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:login')

    def get_form_kwargs(self):
        ctx = super().get_form_kwargs()
        ctx['instance'] = self.request.user
        return ctx

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
