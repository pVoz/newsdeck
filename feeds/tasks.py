# feeds/tasks.py
from celery import shared_task

# Reg - Celery uloha(worker log)
@shared_task(name="feeds.tasks.fetch_rss_feeds")
def fetch_rss_feeds():
    # TODO: download/parsu RSS
    return "ok"

@shared_task
def add(x, y):
    return x + y
