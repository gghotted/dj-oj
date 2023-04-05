from django import forms
from django.contrib.auth import authenticate, password_validation
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
            'nickname',
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


class UserProfileChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'email',
            'nickname',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True


class PasswordChangeForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'password1',
            'password2',
        )


class LoginForm(forms.Form):

    email = forms.EmailField(
        label='이메일',
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(),
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        self.user = authenticate(None, email=email, password=password)
        if not self.user:
            raise ValidationError('일치하는 유저 정보가 없습니다')
        
        return self.cleaned_data
