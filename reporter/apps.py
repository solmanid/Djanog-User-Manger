from django.apps import AppConfig


class ReporterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reporter'

    verbose_name = 'Map Report'
    verbose_name_plural = 'Map Reports'
