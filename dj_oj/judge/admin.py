from django.contrib import admin

from judge.models import Judge


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'runtime',
    ]
