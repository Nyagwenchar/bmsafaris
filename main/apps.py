from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = "MB Travels Main App"  # ✅ shows a friendly name in admin

    def ready(self):
        """
        Import signals or perform startup initialization here.
        This ensures signals are registered when the app is loaded.
        """
        try:
            import main.signals  # noqa
        except ImportError:
            pass
