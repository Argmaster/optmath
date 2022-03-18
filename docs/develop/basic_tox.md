# Basic Tox

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

Every complex Python project requires plenty of tools to develop properly, with
tests, quality checks, documentation and all complex build steps. It is
inevitable that all those things will be sooner or later automated with some
scripts.

### And here comes tox

`tox` can be used as a replacement for any kind of bash/batch/make etc.
scripts, allowing to replace them with simple static ini file with possibility
of extending them with dynamic Python code. Such approach has a long list of
advantages:

- built-in isolation of testing environments, via Python virtual environments
- quick and intuitive command line interface
- built-in Python version awareness
- flexibility of environment configuration and creation
- great integration with any set of Python tools
- utility scripts are guaranteed to be multi-platform
- utility scripts gain access to PyPI's huge set of extensions
- ...

With above said, it was obvious decision to choose `tox` for automation at the
very beginning.

______________________________________________________________________

## Basic usage

To invoke single environment with `tox` you have to memorize one simple
command:

```shell
tox -e envname
```

Where `envname` is replaced 1:1 with name of any environments listed in points
below.

______________________________________________________________________

## Environments in this project

Simplicity of creating `tox` managed environments allows us to create highly
specialized environments with very little boilerplate. All important
environments (crucial for development) are listed below:

______________________________________________________________________

### `devenv` - development environment

```shell
tox -e devenv
```

This environment is meant to contain all tools important for continuos
development, including linters, formatters, building tools, packaging tools and
everything else listed in `requirements-dev.txt`

```ini
{% include 'requirements-dev.txt' %}
```

Running this environment will also install pre-commit. To create this
environment and run all associated commands use:

______________________________________________________________________

### `py37`, `py38`, `py39`, `py310`, `pypy37`, `pypy38` - test environments

```shell
tox -e py37
```

```shell
tox -e pypy37
```

etc.

Those environments are specialized in running test suite with appropriate set
of external libraries installed. List of dependencies for release package is
contained in `requirements.txt` file:

```ini
{% include 'requirements.txt' %}
```

minimal set of libraries required for packaging is installed to

```ini
setuptools>=59.6.0
cython==3.0.0a10
pytest==6.2.4c_extension/#cc-extensions
pytest-cov==3.0.0
```

______________________________________________________________________

### `cmake` - C/C++ automated build environment

```shell
tox -e cmake
```

This environment automates process of building C/C++ extension associated with
this package. It is expected that All C/C++ code will be compiled into static
library to be later linked with Cython generated C/C++ interface. Visit
<a href="../c_extension/#cc-extensions">C/C++ Extensions</a> section to learn
more about building C/C++ Extensions.

______________________________________________________________________

### `build-all` and related environments

```shell
tox -e build-all
```

```shell
tox -e build-py37
```

etc.

Environments with **build** prefix are responsible for building release
packages for corresponding python versions (`build-py37` builds for Python 3.7
etc.). Those packages are stored in `dist/` directory. Only wheels are created
because of project source and building system complexity.
