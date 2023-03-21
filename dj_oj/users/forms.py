from django import forms
from django.contrib.auth import password_validation
from django.forms import ValidationError

from users.models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(),
        strip=False,
    )
    
    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
        )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        password_validation.validate_password(password)
        return password

    def clean(self):
        data = super().clean()
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2 and (password1 != password2):
            self.add_error(
                'password2',
                '비밀번호가 일치하지 않습니다'
            )
        
        return data

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data['password1'])
        return super().save(commit)
