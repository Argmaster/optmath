import itertools
import subprocess as sbp
from pathlib import Path
from typing import List

import click

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT_DIR = SCRIPT_DIR / ".."
SOURCE_DIR = REPO_ROOT_DIR / "source"
INTERNAL_C_CPP = SOURCE_DIR / "internal"


@click.command()
def clang_format_all_cli(*args, **kwargs):
    return clang_format_all(*args, **kwargs)


def clang_format_all():
    result = 0
    processes: List[sbp.Popen] = []

    all_c_like_files = itertools.chain(
        INTERNAL_C_CPP.glob("**/*.c*"),
        INTERNAL_C_CPP.rglob("**/*.h*"),
    )
    for file_path in all_c_like_files:
        file_path = str(file_path.resolve(True))
        file_path_lower = file_path.lower()
        if (
            "cmake" not in file_path_lower
            and "external" not in file_path_lower
        ):
            processes.append(sbp.Popen(["clang-format", file_path, "-i"]))
            print(file_path)
    for process in processes:
        process.wait()
        result += process.returncode
    exit(result)


if __name__ == "__main__":
    exit(clang_format_all_cli())
