from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (LoginView, PasswordChangeView, SignupView,
                         UserProfileChangeView)

app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('change-profile/', UserProfileChangeView.as_view(), name='change_profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
