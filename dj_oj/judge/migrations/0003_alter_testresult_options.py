# Generated by Django 4.1.7 on 2023-04-01 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_alter_judge_runtime_alter_judge_test_passed_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testresult',
            options={'ordering': ['number']},
        ),
    ]