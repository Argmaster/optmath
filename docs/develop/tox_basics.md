# Tox basics

## What is tox?

[`tox`](https://tox.wiki/en/latest/index.html) is a generic virtualenv
management and test command line tool you can use for:

- checking that your package installs correctly with different Python versions
  and interpreters

- running your tests in each of the environments, configuring your test tool of
  choice

- acting as a frontend to Continuous Integration servers, greatly reducing
  boilerplate and merging CI and shell-based testing.

## Handy Links

- [To read more about tox, visit it's documentation.](https://tox.wiki/en/latest/index.html)
- [`tox` global settings](https://tox.wiki/en/latest/config.html#tox-global-settings)
- [`tox` environments configuration](https://tox.wiki/en/latest/config.html#tox-environments)
- [`tox` substitutions](https://tox.wiki/en/latest/config.html#substitutions)
- [Generating environments, conditional settings](https://tox.wiki/en/latest/config.html#generating-environments-conditional-settings)
- [Environmental variables](https://tox.wiki/en/latest/config.html#environment-variables)
- [Full tox cli documentation](https://tox.wiki/en/latest/config.html#cli)
- [`tox` examples](https://tox.wiki/en/latest/examples.html)

______________________________________________________________________

## Our perspective

Every complex Python project requires plenty of tools to develop properly
including tests, quality checks, documentation and all complex build steps. It
is inevitable that all those things will be sooner or later automated with some
scripts.

**And here comes tox**

`tox` can be used as a replacement for any kind of `bash`/`batch`/`make`
scripts. Instead of dynamic and error prone scripts, tox uses static ini file
for configuration. Whenever there is need for dynamic content, you can use
multi-platform Python script and invoke it with `tox`.

Using `tox` has a long list of advantages:

- built-in isolation of testing environments via Python virtual environments
- quick and intuitive command line interface
- built-in Python version awareness
- flexibility of environment configuration and creation
- great integration with any set of Python tools
- utility scripts are guaranteed to be multi-platform
- utility scripts gain access to PyPI's huge set of extensions
- ...

With above said, it was obvious decision to choose `tox` for automation.

______________________________________________________________________

## Basic usage

To invoke single environment with `tox` you have to memorize one simple
command:

```shell
tox -e envname
```

Where `envname` is replaced 1:1 with name of any environments listed below.

______________________________________________________________________

## Environments list

Simplicity of creating `tox` managed environments allows us to create highly
specialized environments with minimal boilerplate.

### `devenv`

Stands for development environment (important when using IDE like Visual Studio
Code or PyCharm). When selecting interpreter for your IDE, `devenv` is a right
one to pick.

```shell
tox -e devenv
```

This environment is meant to contain all tools important for continuos
development including linters, formatters, building tools, packaging tools and
everything else listed in `requirements-dev.txt`

```ini
{% include 'requirements-dev.txt' %}
```

Running this environment will also install pre-commit.

To select Python from `devenv` as interpreter in Visual Studio Code, use
`Ctrl + Shift + P` and type `Python: Select Interpreter`, then hit `Enter`,
select `Enter interpreter path`, pick `Find` and navigate to `python.exe` in
`.tox/devenv/bin` (unix) or `.tox/devev/scripts` (windows).

______________________________________________________________________

### `check`

Runs formatters and code quality checkers over your workspace.

```shell
tox -e check
```

______________________________________________________________________

### `pyXX`

Executes full
[test suite](https://en.wikipedia.org/wiki/Test_suite#:~:text=In%20software%20development%2C%20a%20test,some%20specified%20set%20of%20behaviours.){:target="\_blank"}
with corresponding Python interpreter version, denoted by XX numbers. All
available ones are:

- py37
- py38
- py39
- py310
- pypy37
- pypy38

```shell
tox -e py37
```

List of dependencies for release package is contained in `requirements.txt`
file:

```ini
{% include 'requirements.txt' %}
```

minimal set of libraries required for packaging is installed too

```ini
setuptools>=59.6.0
cython==3.0.0a10
pytest==6.2.4c_extension/#cc-extensions
pytest-cov==3.0.0
```

______________________________________________________________________

### `cmake`

Builds C/C++ extension library with cmake and ninja.

```shell
tox -e cmake
```

This environment automates process of building C/C++ extension library
associated with this package. It is expected that all C/C++ code will be
compiled into static library to be later linked with Cython generated C/C++
interface. Visit
[C/C++ Extensions](../c_extension/#cc-extensions){:target="\_blank"} section to
learn more about how C/C++ Extensions work.

______________________________________________________________________

### `docs`

Builds documentation with mkdocs, all generated files are saved to `site/`
folder.

```shell
tox -e docs
```

______________________________________________________________________

### `build-all`

Builds package distribution
[wheels](https://realpython.com/python-wheels/#what-is-a-python-wheel){:target="\_blank"}
for corresponding Python version.

- build-all
- build-py37
- build-py38
- build-py39
- build-py310
- build-pypy37
- build-pypy38

```shell
tox -e build-all
```

```shell
tox -e build-py37
```

Environments with **build** prefix are responsible for building release
packages for corresponding python versions (`build-py37` builds for Python 3.7
etc.) For each test environment (`py37` etc.) there is a corresponding build
environment. Built packages (wheels) are stored in `dist/` directory.

**IMPORTANT**: There is a slight difference between `build-all` and single
`build-pyXX` environment: `build-all` invokes `cmake` env before all
`build-pyXX` envs, but when running `build-pyXX` env manually, `cmake` env is
not invoked, expecting C/C++ extensions libraries to be already compiled (to
avoid duplication of compilation process).

Therefore, to run only single (eg.) `build-py37` properly you have to use:

```shell
tox -e cmake
tox -e build-py37
```

______________________________________________________________________
