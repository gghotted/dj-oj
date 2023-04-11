# Generated by Django 4.1.7 on 2023-04-11 06:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_alter_category_id_alter_categoryrelation_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problems', '0008_difficulty_name_alter_difficulty_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='skil_category',
            field=models.ManyToManyField(blank=True, related_name='problems', to='categories.category', verbose_name='스킬 카테고리'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='passed_users',
            field=models.ManyToManyField(blank=True, related_name='passed_problems', to=settings.AUTH_USER_MODEL, verbose_name='통과한 유저들'),
        ),
    ]
