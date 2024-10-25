import os

from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

app.config_from_object("project.settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Celery debug task."""
    print(f"Request: {self.request!r}")
