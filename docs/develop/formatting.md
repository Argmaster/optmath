# Code formatting

## black

[`black`](https://pypi.org/project/black/){:target="\_blank"} is the
uncompromising Python code formatter. By using it, you agree to cede control
over minutiae of hand-formatting. In return, `black` gives you speed,
determinism, and freedom from pycodestyle nagging about formatting. You will
save time and mental energy for more important matters.

You can view `black` configuration in `pyproject.toml` file, in `[tool.black]`
section. Manual usage valid for this project:

```shell
black .
```

______________________________________________________________________

## isort

[`isort`](https://pypi.org/project/isort/){:target="\_blank"} your imports, so
you don't have to.

`isort` is a Python utility / library to sort imports alphabetically, and
automatically separated into sections and by type.

You can view `isort` configuration in `.isort.cfg` file. Manual usage valid for
this project:

```shell
isort .
```

______________________________________________________________________

## docformatter

[`docformatter`](https://pypi.org/project/docformatter/){:target="\_blank"}
currently automatically formats docstrings to follow a subset of the PEP 257
conventions. Below are the relevant items quoted from PEP 257.

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

## mdformat

[`mdformat`](https://pypi.org/project/mdformat/){:target="\_blank"} is an
opinionated Markdown formatter that can be used to enforce a consistent style
in Markdown files.

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

## clang-format

[Clang-Format](https://clang.llvm.org/docs/ClangFormat.html){:target="\_blank"}
is a C/C++ code formatter. You can view it's configuration in `.clang-format`
file. Manual usage valid for this project:

```shell
clang-format source/internal/**/*.cpp source/internal/**/*.h -i
```

______________________________________________________________________
