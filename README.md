# optmath

# Development

<i>I strongly encourage all the developers to make use of Visual Studio Code
for development purposes. You can ask me If you encounter any difficulties with
setup.

<div style="text-align: right"> Krzysztof Wiśniewski </div></i>

[Project structure good practices (ours is still not best one though)](https://docs.pytest.org/en/6.2.x/goodpractices.html)<br/>
[Python documentation](https://docs.python.org/3/)<br/>
[tox documentation](https://tox.wiki/en/latest/)<br/>
[pytest documentation](https://docs.pytest.org/en/6.2.x/contents.html)<br/>
[pytest-cov documentation](https://pytest-cov.readthedocs.io/en/latest/)<br/>
[GitHub Actions documentation](https://docs.github.com/en/actions)<br/>
[black documentation](https://black.readthedocs.io/en/stable/)<br/>

### Python interpreter version

At least `Python 3.7` is required. Nice to have all **Python 3.7 - Python
3.10** major releases for testing purposes, but **you will do just fine with
only Python 3.7**.

## DRY tool for tasks - tox

To avoid painstaking manual typing of sequences of commands, not necessarily
portable script files and not standardized mess with task configuration this
project uses `tox` for running tasks like setting up working environment,
testing on different interpreter versions and everything connected with typing
sequences of commands into command line. You can install `tox` either in some
virtual environment (custom solution) or simply globally with:

```bash
$ python -m pip install tox
```

whichever option you choose, remember that you will need tox for recreating
development environment.

`DISCLAIMER: be aware that on linux, 'python' is usually alias for Python 2.7, and 'python3' is alias for python 3.x, you should use the second one then.`

#### Creating development environment (devenv)

`tox` is configured out-of-the-box thanks to multiple configuration files
located in root directory of this repository. To begin with comfortable
development use:

```bash
$ tox -e devenv
```

Above command will create `devenv` environment in `.tox` folder. You should use
`devenv` during development for lining, formatting, pre-commit, manual pytest
calls etc.

<small> For Windows VSC users: Select .tox/devenv/Scripts/python.exe as your
interpreter. </small>

[Check tox documentation if you want to know more.](https://tox.wiki/en/latest/)

#### Running test suite with tox

Test suite can be ran with in multiple environments featuring different
versions of interpreter:

`py37` - [CPython 3.7](https://www.python.org/downloads/release/python-379/)
_(last with binary distribution)_

`py38` - [CPython 3.8](https://www.python.org/downloads/release/python-3810/)
_(last with binary distribution)_

`py39` - [CPython 3.9](https://www.python.org/downloads/release/python-399/)
**_(bugfixes till 2022-04-05)_**

`py310` - [CPython 3.10](https://www.python.org/downloads/release/python-3102/)
**_(bugfixes till 2023-04-04)_**

`pypy37` - [PyPy v7.3.7](https://www.pypy.org/download.html) - Python 3.7
compatible

`pypy38` - [PyPy v7.3.7](https://www.pypy.org/download.html) - Python 3.8
compatible

To run above environments you have to install corresponding Python versions
manually on your system. Interpreters have to be available in PATH.

It is possible to run sequentially all of above environments with:

```bash
$ tox
```

Above one is rather hard to use during development, because not all of the
tests are guarenteed be executed quickly, so running them multiple times just
to see single result is waste of time.

That's why it is possible to run test suite for single python release with:

```bash
$ tox -e {envname}
```

#### Test coverage reports

Test coverage reports are created after running test suite with tox. Created
reports are saved in `coverage/{envname}_htmlcov/`.

#### Running single file with pytest

[pytest cli documentation](https://docs.pytest.org/en/6.2.x/reference.html#command-line-flags)<br/>
To run single file with pytest use

```bash
pytest {test_file_path} -rP
```

for example



#### Common pytest command line args explanation

- `-rP` forwards test output to console, useful for fast debugging.
- `-rx` default, output only of failed tests
- `-v/--verbose` for verbose output
- `--cov` for coverage report
- `--cov-report=term-missing` sets report type

for example:

```bash
pytest tests\test_sub_dir\test_file.py -rP
```
