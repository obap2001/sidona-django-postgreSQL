from django.apps import AppConfig


class BaseHtmlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_html'
