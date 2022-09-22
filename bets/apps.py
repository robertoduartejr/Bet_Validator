from django.apps import AppConfig


class BetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bets'

    def ready(self):
        print('Starting Scheduler ...')
        from .bets_scheduler import bets_updater
        bets_updater.start()