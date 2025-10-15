from django.core.management.base import BaseCommand
from feeds.tasks import fetch_rss_feeds


class Command(BaseCommand):
    help = "Fetch articles from all active RSS sources."

    def handle(self, *args, **options):
        # vol.task
        created = fetch_rss_feeds()
        self.stdout.write(self.style.SUCCESS(f"Imported {created} new articles"))
