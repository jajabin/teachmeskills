from datetime import timedelta, datetime

from django.db import models


def calculate_stats(page, stats_content, start_date, count_days) -> int:
    visit_counter = 0
    for stat in stats_content:
        if stat['url'] == page:
            for day_counter in range(0, count_days + 1):
                day = start_date - timedelta(days=day_counter)
                if stat['date'] == day:
                    visit_counter += 1
    return visit_counter


class StatsModel(models.Model):
    url = models.URLField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    @classmethod
    def get_stats(cls):
        # stats = StatsModel.objects.values().get(pk=1)
        db = StatsModel.objects.values()
        pages = StatsModel.objects.values('url').distinct()
        stats_content = []
        for stat in db:
            stats_content.append(stat)

        today = datetime.today().date()
        stats = []
        for page in pages:
            stat = {"page": page['url'],
                    "today": calculate_stats(page['url'], stats_content, today, 0),
                    "yesterday": calculate_stats(page['url'], stats_content, today - timedelta(days=1), 0),
                    "week": calculate_stats(page['url'], stats_content, today, 7),
                    "month": calculate_stats(page['url'], stats_content, today, 30)}
            stats.append(stat)

        return stats
