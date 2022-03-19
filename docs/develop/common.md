# Common tools

## MkDocs

[MkDocs](https://www.mkdocs.org/) is a fast, simple and downright gorgeous
static site generator that's geared towards building project documentation.
Documentation source files are written in Markdown, and configured with a
single YAML configuration file. Start by reading the introductory tutorial,
then check the User Guide for more information.

- [Their web page](https://www.mkdocs.org/)
- [User guide](https://www.mkdocs.org/user-guide/)

We are also using
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme for
documentation which is a separate package.

- [Their web page](https://squidfunk.github.io/mkdocs-material/)
- [Reference](https://squidfunk.github.io/mkdocs-material/reference/)

```
Usage: mkdocs [OPTIONS] COMMAND [ARGS]...

  MkDocs - Project documentation with Markdown.

Options:
  -V, --version  Show the version and exit.
  -q, --quiet    Silence warnings
  -v, --verbose  Enable verbose output
  -h, --help     Show this message and exit.

Commands:
  build      Build the MkDocs documentation
  gh-deploy  Deploy your documentation to GitHub Pages
  new        Create a new MkDocs project
  serve      Run the builtin development server
```

______________________________________________________________________

### Live server

```shell
mkdocs serve
```

Runs live development server, all changes are immediately visible in web
browser, web page is automatically reloaded. Live server is by default
available at `http://127.0.0.1:8000/`

Full CLI help:

```
Usage: mkdocs serve [OPTIONS]

Run the builtin development server

Options:
-a, --dev-addr <IP:PORT>        IP address and port to serve documentation
                                locally (default: localhost:8000)
--livereload                    Enable the live reloading in the development
                                server (this is the default)
--no-livereload                 Disable the live reloading in the
                                development server.
--dirtyreload                   Enable the live reloading in the development
                                server, but only re-build files that have
                                changed
--watch-theme                   Include the theme in list of files to watch
                                for live reloading. Ignored when live reload
                                is not used.
-f, --config-file FILENAME      Provide a specific MkDocs config
-s, --strict                    Enable strict mode. This will cause MkDocs
                                to abort the build on any warnings.
-t, --theme [material|mkdocs|readthedocs]
                                The theme to use when building your
                                documentation.
--use-directory-urls / --no-directory-urls
                                Use directory URLs when building pages (the
                                default).
-q, --quiet                     Silence warnings
-v, --verbose                   Enable verbose output
-h, --help                      Show this message and exit.
```

______________________________________________________________________

### Build documentation

```shell
mkdocs build
```

Builds documentation, all generated files are by default saved to `site/`
folder.

Full CLI help:

```
Usage: mkdocs build [OPTIONS]

Build the MkDocs documentation

Options:
-c, --clean / --dirty           Remove old files from the site_dir before
                                building (the default).
-f, --config-file FILENAME      Provide a specific MkDocs config
-s, --strict                    Enable strict mode. This will cause MkDocs
                                to abort the build on any warnings.
-t, --theme [mkdocs|material|readthedocs]
                                The theme to use when building your
                                documentation.
--use-directory-urls / --no-directory-urls
                                Use directory URLs when building pages (the
                                default).
-d, --site-dir PATH             The directory to output the result of the
                                documentation build.
-q, --quiet                     Silence warnings
-v, --verbose                   Enable verbose output
-h, --help                      Show this message and exit.
```

______________________________________________________________________

## Code formatting

### black

[`black`](https://pypi.org/project/black/) is the uncompromising Python code
formatter. By using it, you agree to cede control over minutiae of
hand-formatting. In return, `black` gives you speed, determinism, and freedom
from pycodestyle nagging about formatting. You will save time and mental energy
for more important matters.

You can view `black` configuration in `pyproject.toml` file, in `[tool.black]`
section. Manual usage valid for this project:

```shell
black .
```

______________________________________________________________________

### isort

[`isort`](https://pypi.org/project/isort/) your imports, so you don't have to.

`isort` is a Python utility / library to sort imports alphabetically, and
automatically separated into sections and by type.

You can view `isort` configuration in `.isort.cfg` file. Manual usage valid for
this project:

```shell
isort .
```

______________________________________________________________________

### docformatter

[`docformatter`](https://pypi.org/project/docformatter/) currently
automatically formats docstrings to follow a subset of the PEP 257 conventions.
Below are the relevant items quoted from PEP 257.

- For consistency, always use triple double quotes around docstrings.
- Triple quotes are used even though the string fits on one line.
- Multi-line docstrings consist of a summary line just like a one-line
  docstring, followed by a blank line, followed by a more elaborate
  description.
- Unless the entire docstring fits on a line, place the closing quotes on a
  line by themselves.

`docformatter` also handles some of the PEP 8 conventions.

- Don’t write string literals that rely on significant trailing whitespace.
  Such trailing whitespace is visually indistinguishable and some editors (or
  more recently, reindent.py) will trim them.

Manual usage valid for this project:

```shell
docformatter -r source/ scripts/ --in-place --docstring-length 75 75 -e .tox,.eggs,build,dist,typings,.temp
```

______________________________________________________________________

### mdformat

[`mdformat`](https://pypi.org/project/mdformat/) is an opinionated Markdown
formatter that can be used to enforce a consistent style in Markdown files.

The features/opinions of the formatter include:

- Consistent indentation and whitespace across the board
- Always use ATX style headings
- Move all link references to the bottom of the document (sorted by label)
- Reformat indented code blocks as fenced code blocks
- Use 1. as the ordered list marker if possible, also for noninitial list items

You can view `mdformat` configuration in `.mdformat.toml` file. Manual usage
valid for this project:

```shell
mdformat docs
```

______________________________________________________________________

### clang-format

[Clang-Format](https://clang.llvm.org/docs/ClangFormat.html) is a C/C++ code
formatter. You can view it's configuration in `.clang-format` file. Manual
usage valid for this project:

```shell
clang-format source/internal/**/*.cpp source/internal/**/*.h -i
```

______________________________________________________________________

## Code quality checks

### flake8

[Flake8](https://pypi.org/project/flake8/) is a wrapper around these tools:

- [PyFlakes](https://pypi.org/project/pyflakes/) which checks Python source
  files for errors.
- [pycodestyle](https://pypi.org/project/pycodestyle/), a tool to check your
  Python code against some of the style conventions in PEP 8.
- [Ned Batchelder’s McCabe](https://pypi.org/project/mccabe/) script for
  checking McCabe complexity.

[See list of awesome flake8 plugins](https://github.com/DmytroLitvinov/awesome-flake8-extensions)

List of included 3rd-party plugins:

- [flake8-alphabetize](https://pypi.org/project/flake8-alphabetize/) - checker
  for alphabetizing import and **all**.
- [flake8-alfred](https://pypi.org/project/flake8-alfred/) - warn on
  unsafe/obsolete symbols.
- [flake8-broken-line](https://pypi.org/project/flake8-broken-line/) - forbid
  backslashes () for line breaks.
- [flake8-bugbear](https://pypi.org/project/flake8-bugbear/) - finding likely
  bugs and design problems in your program.
- [flake8-builtins](https://pypi.org/project/flake8-builtins/) - check for
  python builtins being used as variables or parameters.
- [flake8-comprehensions](https://pypi.org/project/flake8-comprehensions/) -
  check for invalid list/set/dict comprehensions.
- [flake8-functions-names](https://pypi.org/project/flake8-functions-names/) -
  validates function names, decomposition and conformity with annotations.
  Conventions from
  [here](https://melevir.medium.com/python-functions-naming-the-algorithm-74320a18278d)
  and
  [here](https://melevir.medium.com/python-functions-naming-tips-376f12549f9).
- [flake8-eradicate](https://pypi.org/project/flake8-eradicate/) - find
  commented out (or so called "dead") code.
- [flake8-printf-formatting](https://pypi.org/project/flake8-printf-formatting/)
  \- forbids printf-style string formatting
- [flake8-pytest-style](https://pypi.org/project/flake8-pytest-style/) -
  checking common style issues or inconsistencies with pytest-based tests.
- [flake8-simplify](https://pypi.org/project/flake8-simplify/) - helps you
  simplify your code.
- [pep8-naming](https://pypi.org/project/pep8-naming/) - check your code
  against PEP 8 naming conventions.
- [flake8-functions](https://pypi.org/project/flake8-functions/) - report on
  issues with functions.
- [flake8-cognitive-complexity](https://pypi.org/project/flake8-cognitive-complexity/)
  \- validates cognitive functions complexity.
- [flake8-expression-complexity](https://pypi.org/project/flake8-expression-complexity/)
  \- validates expression complexity and stops you from creating monstrous
  multi-line expressions.
