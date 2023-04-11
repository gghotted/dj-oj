# Generated by Django 4.1.7 on 2023-04-11 00:45

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(help_text='<ul><li>글자 수는 4~16 이어야 합니다</li><li>문자, 숫자, @ . + - _ 로 이루어져야 합니다</li></ul>', max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(4), django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='닉네임'),
        ),
    ]