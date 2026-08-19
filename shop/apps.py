from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        # ready() викликається один раз при старті Django.
        # Імпортуємо signals.py щоб Django "підписався" на наші сигнали.
        # Якщо не імпортувати тут — сигнали просто не спрацюють.
        import shop.signals  # noqa: F401
