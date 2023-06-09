# Generated by Django 4.1.7 on 2023-03-26 07:40

import core.fields
import django.core.validators
from django.db import migrations
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerimage',
            name='zip_file',
            field=core.fields.TemporaryZipFileField(help_text='루트 폴더에 Dockerfile을 포함해야합니다', storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='media/docker_images/', validators=[django.core.validators.FileExtensionValidator(['zip'])], verbose_name='zip 파일'),
        ),
    ]
