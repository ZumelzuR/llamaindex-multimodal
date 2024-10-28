import os
import re


def create_meta_from_name(file_path):
    if not isinstance(file_path, str):
        raise ValueError("file_name must be a string")

    file_name = os.path.basename(file_path)
    pattern = re.compile(r"^[a-zA-Z0-9-]+__[a-zA-Z0-9--]+_\d+\.[a-zA-Z0-9]+$")
    if not pattern.match(file_name):
        raise ValueError("file name format is incorrect")

    try:
        item_part = file_name.split("__")[0]
        page_part = file_path.split("_")[-1].split(".")[0]
        return {
            "file_path": file_path,
            "item": item_part,
            "page": page_part,
        }
    except (IndexError, ValueError):
        raise ValueError("file name format is incorrect")
