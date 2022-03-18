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
    check_ninja_available()
    refresh_build_dir()
    chdir(BUILD_DIR)
    run_cmake()
    run_ninja()


def check_ninja_available():
    try:
        sbp.check_output(["ninja", "--version"])
    except FileNotFoundError:
        print(
            "\n\n This project requires ninja build system for compilation of C/C++ modules with cmake. \n\n"
        )
        exit(NO_NINJA_FOUND)


def refresh_build_dir():
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(0o777, True, True)


def run_cmake():
    process = sbp.Popen(["cmake", "..", "-G", "Ninja", "--clean-first"])
    process.wait()
    assert process.returncode == 0, process.returncode


def run_ninja():
    process = sbp.Popen(["ninja"])
    process.wait()
    assert process.returncode == 0, process.returncode


if __name__ == "__main__":
    exit(main())
