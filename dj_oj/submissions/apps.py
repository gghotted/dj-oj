from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'submissions'

    # def ready(self):
    #     from submissions import rules
