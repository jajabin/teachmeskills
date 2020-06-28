import json
from pathlib import Path
from typing import Dict


def update_json_file(user_data, content_file: str):
    content = read_json_file(content_file)
    content.update(user_data)  # what does update ???
    write_json_file(content_file, content)


def read_json_file(path: str) -> Dict:
    file_path = Path(__file__).parent.parent.resolve() / path
    try:
        with file_path.open("r", encoding="utf-8") as usf:
            return json.load(usf)   #what does load?
    except (json.JSONDecodeError, FileNotFoundError):
        return {}   #return error!!!


def write_json_file(path: str, data: Dict) -> None:
    file_path = Path(__file__).parent.parent.resolve() / path
    with file_path.open("w") as usf:
        json.dump(data, usf)
