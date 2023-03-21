from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import RedirectURLMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import LoginForm, UserCreationForm


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
