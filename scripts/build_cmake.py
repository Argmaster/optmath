#!/usr/bin/python3
import shutil
import subprocess as sbp
from os import chdir
from pathlib import Path
from typing import Tuple

import click

SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT_DIR = SCRIPTS_DIR.parent
C_SOURCE_DIR = REPO_ROOT_DIR / "internal"
BUILD_DIR = (REPO_ROOT_DIR / "build").absolute().resolve()
PYTHON_PACKAGE_DIR = REPO_ROOT_DIR / "source" / "optmath"


NO_NINJA_FOUND = -0xFF


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--clean/--no-clean",
    default=True,
    help=(
        "Do a 'clean' build - remove all already "
        "compiled code and build everything again."
    ),
)
@click.option(
    "--skip/--no-skip",
    default=False,
    help="Skip whole build process - makes this script noop.",
)
@click.option("--release", "is_release", flag_value=True, default=True)
@click.option("--debug", "is_release", flag_value=False)
@click.argument("cmake_args", nargs=-1, type=click.UNPROCESSED)
def build_cmake_cli(*args, **kwargs):
    return build_cmake(*args, **kwargs)


def build_cmake(
    skip: bool = False,
    clean: bool = True,
    is_release: bool = True,
    cmake_args: Tuple[str, ...] = (),
):
    """Compile C/C++ extension using cmake and ninja."""
    if skip:
        print("Skipped C/C++ extension building sequence due to --skip flag.")
        return 0

    try:
        _build_extension(clean, is_release, cmake_args)

    except AssertionError as e:
        return e.args[0]
    else:
        return 0


def _build_extension(
    clean: bool,
    is_release: bool,
    cmake_args: Tuple[str, ...],
):
    if clean:
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(0o777, True, True)
    chdir(BUILD_DIR)
    _run_cmake_generate(is_release, cmake_args)
    _run_ninja()


def _run_cmake_generate(
    is_release: bool,
    cmake_args: Tuple[str, ...],
):
    process = sbp.Popen(
        [
            "cmake",
            "..",
            "-G",
            "Ninja",
            f"-DCMAKE_BUILD_TYPE={'Release' if is_release else 'Debug'}",
            *cmake_args,
        ],
    )
    process.wait()
    assert (
        process.returncode == 0
    ), f"CMake failed with return code {process.returncode}"


def _run_ninja():
    process = sbp.Popen(["ninja"])
    process.wait()
    assert (
        process.returncode == 0
    ), f"Ninja failed with return code {process.returncode}"


if __name__ == "__main__":
    exit(build_cmake_cli())
