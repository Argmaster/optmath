# noqa: D100
import shutil
import subprocess as sbp
from os import chdir
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT_DIR = SCRIPTS_DIR.parent
C_SOURCE_DIR = REPO_ROOT_DIR / "internal"
BUILD_DIR = REPO_ROOT_DIR / "build"
PYTHON_PACKAGE_DIR = REPO_ROOT_DIR / "source" / "optmath"


NO_NINJA_FOUND = -0xFF


def main():
    """Compile C/C++ extension using cmake and ninja."""
    _check_ninja_available()
    _refresh_build_dir()
    chdir(BUILD_DIR)
    _run_cmake()
    _run_ninja()


def _check_ninja_available():
    try:
        sbp.check_output(["ninja", "--version"])
    except FileNotFoundError:
        print(
            "\n\n This project requires ninja build system for compilation of C/C++ modules with cmake. \n\n"
        )
        exit(NO_NINJA_FOUND)


def _refresh_build_dir():
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(0o777, True, True)


def _run_cmake():
    process = sbp.Popen(["cmake", "..", "-G", "Ninja", "--clean-first"])
    process.wait()
    assert process.returncode == 0, process.returncode


def _run_ninja():
    process = sbp.Popen(["ninja"])
    process.wait()
    assert process.returncode == 0, process.returncode


if __name__ == "__main__":
    exit(main())
