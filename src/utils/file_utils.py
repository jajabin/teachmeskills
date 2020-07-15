from pathlib import Path


def get_file_contents(file: Path, file_format="utf-8") -> str:
    if not file.is_file():
        raise FileNotFoundError
    with file.open("r", encoding=file_format) as file_src:
        content = file_src.read()
    return content
