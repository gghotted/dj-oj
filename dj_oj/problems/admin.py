import importlib.machinery
import os

import docker
from django.contrib import admin
from django.db.models import Count

from problems.models import (Category, Difficulty, DockerImage, EditableFile,
                             Problem)


@admin.register(DockerImage)
class DockerImageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tag',
    ]

    def save_model(self, request, obj, form, change):
        obj.save()
        with obj.zip_file.unzip() as path:
            client = docker.from_env()
            client.images.build(
                path=str(path),
                tag=obj.tag,
            )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                'created_by',
                'base_docker_image',
                'number',
                'volume_tree',
            ]
        else:
            return [
                'created_by',
                'is_tested',
                'volume_tree',
            ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user

        obj.save()

        if 'test_file' in form.changed_data:

            with obj.test_file.unzip() as path:
                volume_path = str(path / 'volume')
                obj.volume_tree = os.popen('tree  --dirsfirst %s' % volume_path).read()
                obj.save()

                test = importlib.machinery.SourceFileLoader(
                    'test%d' % obj.number, str(path / 'test/__init__.py')
                ).load_module()
                
                obj.editable_files.all().delete()
                for name, detail in test.REQUIRED_INPUT_FILES.items():
                    EditableFile.objects.create(
                        name=name,
                        path=detail['full_path'],
                        contents=detail['init'].read_text(),
                        problem=obj,
                    )
