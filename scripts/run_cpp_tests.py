import os
import subprocess as sbp
from pathlib import Path

import click

SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT_DIR = SCRIPTS_DIR.parent
C_SOURCE_DIR = REPO_ROOT_DIR / "internal"
BUILD_DIR = (REPO_ROOT_DIR / "build").absolute().resolve()
PYTHON_PACKAGE_DIR = REPO_ROOT_DIR / "source" / "optmath"


@click.command()
def run_cpp_tests_cli(*args, **kwargs):
    return run_cpp_tests(*args, **kwargs)


def run_cpp_tests():
    # move to build dir, expect build dir to exist
    assert BUILD_DIR.exists(), (
        "Build directory doesn't exist, build C++ "
        "library first. (check docs for how-to)"
    )
    os.chdir(BUILD_DIR)
    # run ctest - again, expects it to be available
    process = sbp.Popen(
        ["ctest", "-j6", "-C", "Debug", "-T", "test", "--output-on-failure"],
    )
    process.wait()
    assert (
        process.returncode == 0
    ), f"CTest failed with return code {process.returncode}"
    return 0


if __name__ == "__main__":
    exit(run_cpp_tests_cli())
