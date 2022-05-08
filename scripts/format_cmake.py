#!/usr/bin/python3
import logging
import subprocess as sbp
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).parent.parent


def format_cmake():
    logging.getLogger().setLevel(logging.INFO)

    for file in PROJECT_ROOT.rglob("CMakeLists.txt"):
        file_path = str(file)
        if "external" not in file_path:
            logging.info(f"Formatting {file_path}")
            sbp.run(["cmake-format", str(file_path), "-i"])


if __name__ == "__main__":
    format_cmake()
