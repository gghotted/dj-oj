# Generated by Django 4.1.7 on 2023-04-01 21:35

import django_extensions.db.fields
from django.db import migrations


def set_uuid(apps, schema_editor):
    Submission = apps.get_model('submissions', 'Submission')
    for submission in Submission.objects.all():
        submission.save()


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0005_submission_uuid'),
    ]

    operations = [
        migrations.RunPython(set_uuid, lambda a, s: None),
        migrations.AlterField(
            model_name='submission',
            name='uuid',
            field=django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=12, unique=True, verbose_name='uuid'),
        ),
    ]
