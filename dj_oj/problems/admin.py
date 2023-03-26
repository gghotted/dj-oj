from tempfile import TemporaryDirectory
from zipfile import ZipFile

import docker
from django.contrib import admin

from problems.models import DockerImage


@admin.register(DockerImage)
class DockerImageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tag',
    ]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            
            with obj.zip_file.unzip() as path:
                client = docker.from_env()
                client.images.build(
                    path=str(path),
                    tag=obj.tag,
                )
