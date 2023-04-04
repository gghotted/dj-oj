# Generated by Django 4.1.7 on 2023-04-03 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_initial_rank(apps, _):
    User = apps.get_model('users', 'User')
    Rank = apps.get_model('ranks', 'Rank')
    ranks = []
    for user in User.objects.all():
        ranks.append(Rank(user=user))
    Rank.objects.bulk_create(ranks)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('rank', models.PositiveBigIntegerField(null=True, verbose_name='랭크')),
                ('score', models.PositiveIntegerField(null=True, verbose_name='점수')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.RunPython(create_initial_rank, lambda a, _: None),
    ]