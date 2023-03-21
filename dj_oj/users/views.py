from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserCreationForm


class SignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
