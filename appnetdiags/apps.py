from django.apps import AppConfig


class AppnetdiagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appnetdiags'

    def ready(self):
        import appnetdiags.signals
