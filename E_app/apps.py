from django.apps import AppConfig


class EAppConfig(AppConfig):
    name = 'E_app'

    def ready(self):
        import E_app.signals
