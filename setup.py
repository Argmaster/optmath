import re
from glob import glob
from os.path import basename, splitext
from pathlib import Path
from typing import List

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

REPOSITORY_ROOT_DIR = Path(__file__).parent
PACKAGE_NAME = "optmath"
SOURCE_DIR = REPOSITORY_ROOT_DIR / "source" / PACKAGE_NAME

VERSION_REGEX = re.compile(r'''__version__.*?=.*?"(\d+\.\d+\.\d+.*?)"''')


def fetch_long_description():
    return (
        f"{fetch_utf8_content(REPOSITORY_ROOT_DIR / 'README.md')}\n"
        f"{fetch_utf8_content(REPOSITORY_ROOT_DIR / 'CHANGELOG.md')}"
    )


def fetch_utf8_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def fetch_requirements(file_path: str) -> List[str]:
    requirements_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        for requirement in file.readlines():
            requirement = requirement.strip()
            if requirement.startswith("-r"):
                requirements_list.extend(
                    fetch_requirements(
                        REPOSITORY_ROOT_DIR / requirement.lstrip("-r").strip()
                    )
                )
            else:
                requirements_list.append(requirement)
        return requirements_list


def fetch_package_python_modules(glob_pattern: str) -> List[str]:
    return [splitext(basename(path))[0] for path in glob(str(glob_pattern))]


def fetch_version(init_file: Path) -> str:
    with init_file.open("r", encoding="utf-8") as file:
        return VERSION_REGEX.search(file.read()).group(1)


NAME = PACKAGE_NAME
VERSION = fetch_version(SOURCE_DIR / "__init__.py")
LICENSE_NAME = "MIT"
SHORT_DESCRIPTION = "C accelerated Python math library"
LONG_DESCRIPTION = fetch_utf8_content("README.md")
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
INSTALL_REQUIRES = fetch_requirements(REPOSITORY_ROOT_DIR / "requirements.txt")
EXTRAS_REQUIRE_DEV = fetch_requirements(
    REPOSITORY_ROOT_DIR / "requirements-dev.txt"
)
AUTHOR = "optmath team"
AUTHOR_EMAIL = "argmaster.world@gmail.com"
URL = "https://github.com/Argmaster/optmath"
PACKAGES = find_packages(where="source")
PACKAGE_DIR = {"": "source"}
PACKAGE_PYTHON_MODULES = fetch_package_python_modules(SOURCE_DIR / "*.py")
INCLUDE_PACKAGE_DATA = True
ZIP_SAFE = False
CLASSIFIERS = [
    # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: Unix",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Utilities",
]
PROJECT_URLS = {}
KEYWORDS = [
    "python-3",
    "python-3.7",
    "python-3.8",
    "python-3.9",
    "python-3.10",
]
EXTRAS_REQUIRE = {"dev": EXTRAS_REQUIRE_DEV}
ENTRY_POINTS = {
    # "console_scripts": [
    #    "optmath.__main__:main"
    # ]
}
PYTHON_REQUIREMENTS = ">=3.7"


MODULES = cythonize(
    Extension(
        "optmath.internal.interface",
        sources=["source/optmath/internal/interface.pyx"],
        include_dirs=["./source/internal/include/"],
        library_dirs=["./build/source/internal/"],
        libraries=["optmath"],
        language="c++",
    )
)


def run_setup_script():
    setup(
        name=NAME,
        version=VERSION,
        license=LICENSE_NAME,
        description=SHORT_DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=PACKAGES,
        package_dir=PACKAGE_DIR,
        py_modules=PACKAGE_PYTHON_MODULES,
        include_package_data=INCLUDE_PACKAGE_DATA,
        zip_safe=ZIP_SAFE,
        classifiers=CLASSIFIERS,
        project_urls=PROJECT_URLS,
        keywords=KEYWORDS,
        python_requires=PYTHON_REQUIREMENTS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        entry_points=ENTRY_POINTS,
        ext_modules=MODULES,
        package_data={"optmath.internal.interface": ["*.so"]},
    )


if __name__ == "__main__":
    run_setup_script()
