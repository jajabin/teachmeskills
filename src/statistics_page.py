from datetime import datetime, timedelta
from src.json_utils import *
from src.responds import *
from src.user_utils import *
from src.errors import *
from src.file_utils import *
from src.night_mode import *

PROJECT_DIR = Path(__file__).parent.parent.resolve()
VISIR_COUNTERS = PROJECT_DIR / "visit_counters.json"


def increment_page_visit(self, endpoint: str) -> None:
    today = str(datetime.today().date())
    statistics_content = read_json_file(VISIR_COUNTERS)

    if endpoint not in statistics_content:
        statistics_content[endpoint] = {}
    if today not in statistics_content[endpoint]:
        statistics_content[endpoint][today] = 0

    statistics_content[endpoint][today] += 1
    write_json_file(VISIR_COUNTERS, statistics_content)


def calculate_stats(page_statistics, start_date, count_days) -> int:
    visit_counter = 0
    for day_counter in range(0, count_days + 1):
        day = str(start_date - timedelta(days=day_counter))
        if day in page_statistics:
            visit_counter += page_statistics[day]

    return visit_counter


def get_page_statistics(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_statistics,
        "POST": save_page_statistics,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/statistics")
    else:
        raise MethodNotAllowed


def show_page_statistics(self, _method, _endpoint) -> None:
    statistics_content = read_json_file(VISIR_COUNTERS)

    today = datetime.today().date()
    stats = {}
    for page in statistics_content:
        stats[page] = {}
        stats[page]["today"] = calculate_stats(statistics_content[page], today, 0)
        stats[page]["yesterday"] = calculate_stats(statistics_content[page], today - timedelta(days=1), 0)
        stats[page]["week"] = calculate_stats(statistics_content[page], today, 7)
        stats[page]["month"] = calculate_stats(statistics_content[page], today, 30)

    html = """<tr>
            <th>Page</th>
            <th>Today</th>
            <th>Yesterday</th> 
            <th>Week</th>
            <th>Month</th>
           </tr>"""
    for endpoint, visits in stats.items():
        html += f"<tr><td>{endpoint}</td>"
        for data, count in visits.items():
            html += f"<td>{count}</td>"
    html += "</tr>"

    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)

    msg = get_file_contents("pages/statistics.html").format(stats=html, **user_session[user_id])
    respond_200(self, msg, "text/html")


def save_page_statistics(self, endpoint: str, redirect_to: str):
    switcher = {
        "/statistics/set_night_mode": set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](self, redirect_to)
    else:
        raise MethodNotAllowed