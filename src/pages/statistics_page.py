from datetime import datetime, timedelta

import src.common.errors as errors
import src.common.night_mode as nm
import src.common.paths as paths
import src.common.responds as responds
import src.utils.file_utils as fu
import src.utils.json_utils as ju
import src.utils.user_utils as uu


def increment_page_visit(endpoint: str) -> None:
    today = str(datetime.today().date())
    statistics_content = ju.read_json_file(paths.VISIT_COUNTERS)

    if endpoint not in statistics_content:
        statistics_content[endpoint] = {}
    if today not in statistics_content[endpoint]:
        statistics_content[endpoint][today] = 0

    statistics_content[endpoint][today] += 1
    ju.write_json_file(paths.VISIT_COUNTERS, statistics_content)


def calculate_stats(page_statistics, start_date, count_days) -> int:
    visit_counter = 0
    for day_counter in range(0, count_days + 1):
        day = str(start_date - timedelta(days=day_counter))
        if day in page_statistics:
            visit_counter += page_statistics[day]

    return visit_counter


def get_page_statistics(server_inst, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_statistics,
        "POST": save_page_statistics,
    }
    if method in switcher:
        switcher[method](server_inst, endpoint, "/statistics/")
    else:
        raise errors.MethodNotAllowed


def show_page_statistics(server_inst, _endpoint, _redirect_to) -> None:
    statistics_content = ju.read_json_file(paths.VISIT_COUNTERS)

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

    user_id = uu.get_user_id(server_inst)
    user_session = uu.read_user_session(user_id)

    msg = fu.get_file_contents(paths.STATISTICS_HTML).format(stats=html, **user_session[user_id])
    responds.respond_200(server_inst, msg, "text/html")


def save_page_statistics(server_inst, endpoint: str, redirect_to: str):
    switcher = {
        "/statistics/set_night_mode": nm.set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](server_inst, redirect_to)
    else:
        raise errors.MethodNotAllowed