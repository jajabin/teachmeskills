from datetime import datetime
from applications.stats.models import StatsModel


def increment_visit(view):
    class Visit(view):
        def setup(self, *args, **kwargs):
            super().setup(*args, **kwargs)

            visit = StatsModel()
            visit.url = self.request.path
            visit.date = str(datetime.today().date())
            visit.save()

    return Visit


def increment_page_visit(endpoint) -> None:
    pass
#     today = str(datetime.today().date())
#     statistics_content = ju.read_json_file(paths.VISIT_COUNTERS)
#
#     if endpoint not in statistics_content:
#         statistics_content[endpoint] = {}
#     if today not in statistics_content[endpoint]:
#         statistics_content[endpoint][today] = 0
#
#     statistics_content[endpoint][today] += 1
#     ju.write_json_file(paths.VISIT_COUNTERS, statistics_content)

