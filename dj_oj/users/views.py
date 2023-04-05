from copy import copy

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import RedirectURLMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import (LoginForm, PasswordChangeForm, UserCreationForm,
                         UserProfileChangeForm)


class SignupView(CreateView):
    template_name = 'core/simple_form_page.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            title='회원가입',
            btn_name='가입'
        )


class LoginView(RedirectURLMixin, FormView):
    template_name = 'core/simple_form_page.html'
    form_class = LoginForm
    next_page = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            title='로그인',
            btn_name='로그인'
        )


class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'core/simple_form_page.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:login')

    def get_form_kwargs(self):
        ctx = super().get_form_kwargs()
        ctx['instance'] = self.request.user
        return ctx

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            '성공적으로 변경되었습니다',
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            title='비밀번호 변경',
            btn_name='변경'
        )


class UserProfileChangeView(LoginRequiredMixin, FormView):
    template_name = 'core/simple_form_page.html'
    form_class = UserProfileChangeForm
    success_url = reverse_lazy('problems:list')

    def get_form_kwargs(self):
        ctx = super().get_form_kwargs()
        ctx['instance'] = copy(self.request.user)
        return ctx

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            title='프로필 변경',
            btn_name='변경'
        )
