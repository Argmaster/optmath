# Tox basics

> A virtual environment is a Python environment such that the Python interpreter,
> libraries and scripts installed into it are isolated from those installed in other
> virtual environments, and (by default) any libraries installed in a “system” Python,
> i.e., one which is installed as part of your operating system.

## What is tox?

[`tox`](https://tox.wiki/en/latest/index.html) is a generic virtualenv
management and test command line tool you can use for:

-   checking that your package installs correctly with different Python versions
    and interpreters

-   running your tests in each of the environments, configuring your test tool of
    choice

-   acting as a frontend to Continuous Integration servers, greatly reducing
    boilerplate and merging CI and shell-based testing.

## Handy Links

-   [To read more about tox, visit it's documentation.](https://tox.wiki/en/latest/index.html)
-   [`tox` global settings](https://tox.wiki/en/latest/config.html#tox-global-settings)
-   [`tox` environments configuration](https://tox.wiki/en/latest/config.html#tox-environments)
-   [`tox` substitutions](https://tox.wiki/en/latest/config.html#substitutions)
-   [Generating environments, conditional settings](https://tox.wiki/en/latest/config.html#generating-environments-conditional-settings)
-   [Environmental variables](https://tox.wiki/en/latest/config.html#environment-variables)
-   [Full tox cli documentation](https://tox.wiki/en/latest/config.html#cli)
-   [`tox` examples](https://tox.wiki/en/latest/examples.html)

---

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

-   built-in isolation of testing environments via Python virtual environments
-   quick and intuitive command line interface
-   built-in Python version awareness
-   flexibility of environment configuration and creation
-   great integration with any set of Python tools
-   utility scripts are guaranteed to be multi-platform
-   utility scripts gain access to PyPI's huge set of extensions
-   ...

With above said, it was obvious decision to choose `tox` for automation.

---

## Basic usage

To invoke single environment with `tox` you have to memorize one simple
command:

```shell
tox -e envname
```

Where `envname` is replaced 1:1 with name of any environments listed below.

---

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
everything else listed in `requirements-dev.txt` It is really heavy and
expensive to create because of complexity of installation. Every call
of `tox -e devenv` will completely recreate the environment.

!!! Danger "Running tox -e devenv completely reinstalls environment - it's time consuming."

It is designed in such way many due to the fact that during development
there is no need to recreate it until something brakes, and then it's
handy to simplify reinstallation how much possible.

!!! Success "Running this environment will install pre-commit."

To select Python from `devenv` as interpreter in Visual Studio Code, use
`Ctrl + Shift + P` and type `Python: Select Interpreter`, then hit `Enter`,
select `Enter interpreter path`, pick `Find` and navigate to `python.exe` in
`.tox/devenv/bin` (unix) or `.tox/devev/scripts` (windows).

This environment is rather bullet proof in comparison to other non-utility
environments (mainly test runners). It should just install on demand, and
every failure should be considered and fixed permanently.

---

### `check`

Runs formatters and code quality checkers over your workspace.

```shell
tox -e check
```

This environment is lightweight compared to devenv because it installs
dependencies once and completely skips installing a package from this
repository as it does not need it. The operations performed by this
environment are performed in place.

!!! Success "This environment is lightweight, running tox -e check often is fine."

 Similarly to devenv it is bullet proof
in comparison to other non-utility environments (mainly test runners). It
should just install on demand, and every failure should be considered and
fixed permanently.

---

### `pyXX`


!!! Warning "pyXX - test runner envs - they require special care and you are responsible for their well being."

Executes full
[test suite](https://en.wikipedia.org/wiki/Test_suite#:~:text=In%20software%20development%2C%20a%20test,some%20specified%20set%20of%20behaviours.){:target="\_blank"}
with corresponding Python interpreter version, denoted by XX numbers. All
available ones are:

-   py37
-   py38
-   py39
-   py310
-   pypy37
-   pypy38

```shell
tox -e py37
```

!!! Warning "Running `tox -e py37` should be preceded with `tox -e cmake` to build lastest version of C/C++ internals."

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

---

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

---

### `docs`

Builds documentation with mkdocs, all generated files are saved to `site/`
folder.

```shell
tox -e docs
```

---

### `build-all`

Builds package distribution
[wheels](https://realpython.com/python-wheels/#what-is-a-python-wheel){:target="\_blank"}
for corresponding Python version.

-   build-all
-   build-py37
-   build-py38
-   build-py39
-   build-py310
-   build-pypy37
-   build-pypy38

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

---

## Name tags list

```
devenv
cmake
docs
check
py37
py38
py39
py310
pypy37
pypy38
build-all
build-py37
build-py38
build-py39
build-py310
build-pypy37
build-pypy38
```
