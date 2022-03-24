import shutil
import subprocess as sbp
from os import chdir
from pathlib import Path

import click

SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT_DIR = SCRIPTS_DIR.parent
C_SOURCE_DIR = REPO_ROOT_DIR / "internal"
BUILD_DIR = (REPO_ROOT_DIR / "build").absolute().resolve()
PYTHON_PACKAGE_DIR = REPO_ROOT_DIR / "source" / "optmath"


NO_NINJA_FOUND = -0xFF


@click.command()
@click.option("--clean/--no-clean", default=True)
@click.option("--skip/--no-skip", default=False)
def build_cmake_cli(*args, **kwargs):
    return build_cmake(*args, **kwargs)


def build_cmake(skip: bool = False, clean: bool = True):
    """Compile C/C++ extension using cmake and ninja."""
    if skip:
        print("Skipped C/C++ extension building sequence due to --skip flag.")
        return 0

    try:
        _build_extension(clean)

    except AssertionError as e:
        return e.args[0]
    else:
        return 0


def _build_extension(clean: bool):
    if clean:
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(0o777, True, True)
    chdir(BUILD_DIR)
    _run_cmake_generate()
    _run_ninja()


def _run_cmake_generate():
    process = sbp.Popen(["cmake", "..", "-G", "Ninja"])
    process.wait()
    assert process.returncode == 0, process.returncode


def _run_ninja():
    process = sbp.Popen(["ninja"])
    process.wait()
    assert process.returncode == 0, process.returncode


if __name__ == "__main__":
    exit(build_cmake_cli())
