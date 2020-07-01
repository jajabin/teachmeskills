import json
from typing import Dict


def update_json_file(user_data, file: str):
    content = read_json_file(file)
    content.update(user_data)  # what does update ???
    write_json_file(file, content)


def read_json_file(file: str) -> Dict:
    try:
        with file.open("r", encoding="utf-8") as usf:
            return json.load(usf)  # what does load?
    except (json.JSONDecodeError, FileNotFoundError):
        return {}  # return error!!!


def write_json_file(file: str, data: Dict) -> None:
    with file.open("w") as usf:
        json.dump(data, usf)
