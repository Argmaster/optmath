# Code quality checks

## flake8

[Flake8](https://pypi.org/project/flake8/){:target="\_blank"} is a wrapper
around these tools:

- [PyFlakes](https://pypi.org/project/pyflakes/){:target="\_blank"} which
  checks Python source files for errors.
- [pycodestyle](https://pypi.org/project/pycodestyle/){:target="\_blank"}, a
  tool to check your Python code against some of the style conventions in PEP
  8\.
- [Ned Batchelder’s McCabe](https://pypi.org/project/mccabe/){:target="\_blank"}
  script for checking McCabe complexity.

[See list of awesome flake8 plugins](https://github.com/DmytroLitvinov/awesome-flake8-extensions){:target="\_blank"}

**List of included 3rd-party plugins:**

- [flake8-alfred](https://pypi.org/project/flake8-alfred/){:target="\_blank"} -
  warn on unsafe/obsolete symbols.
- [flake8-alphabetize](https://pypi.org/project/flake8-alphabetize/){:target="\_blank"}
  \- checker for alphabetizing import and **all**.
- [flake8-broken-line](https://pypi.org/project/flake8-broken-line/){:target="\_blank"}
  \- forbid backslashes (){:target="\_blank"} for line breaks.
- [flake8-bugbear](https://pypi.org/project/flake8-bugbear/){:target="\_blank"}
  \- finding likely bugs and design problems in your program.
- [flake8-builtins](https://pypi.org/project/flake8-builtins/){:target="\_blank"}
  \- check for python builtins being used as variables or parameters.
- [flake8-comprehensions](https://pypi.org/project/flake8-comprehensions/){:target="\_blank"}
  \- check for invalid list/set/dict comprehensions.
- [flake8-docstrings](https://pypi.org/project/flake8-docstrings/){:target="\_blank"}
  \- uses pydocstyle to check docstrings
- [flake8-eradicate](https://pypi.org/project/flake8-eradicate/){:target="\_blank"}
  \- find commented out (or so called "dead"){:target="\_blank"} code.
- [flake8-functions](https://pypi.org/project/flake8-functions/){:target="\_blank"}
  \- report on issues with functions.
- [flake8-functions-names](https://pypi.org/project/flake8-functions-names/){:target="\_blank"}
  \- validates function names, decomposition and conformity with annotations.
  Conventions from
  [here](https://melevir.medium.com/python-functions-naming-the-algorithm-74320a18278d){:target="\_blank"}
  and
  [here](https://melevir.medium.com/python-functions-naming-tips-376f12549f9){:target="\_blank"}.
- [flake8-printf-formatting](https://pypi.org/project/flake8-printf-formatting/){:target="\_blank"}
  \- forbids printf-style string formatting
- [flake8-pytest-style](https://pypi.org/project/flake8-pytest-style/){:target="\_blank"}
  \- checking common style issues or inconsistencies with pytest-based tests.
- [flake8-simplify](https://pypi.org/project/flake8-simplify/){:target="\_blank"}
  \- helps you simplify your code.
- [pep8-naming](https://pypi.org/project/pep8-naming/){:target="\_blank"} -
  check your code against PEP 8 naming conventions.
- [flake8-expression-complexity](https://pypi.org/project/flake8-expression-complexity/){:target="\_blank"}
  \- validates expression complexity and stops you from creating monstrous
  multi-line expressions.
- [flake8-cognitive-complexity](https://pypi.org/project/flake8-cognitive-complexity/){:target="\_blank"}
  \- validates cognitive functions complexity.

______________________________________________________________________

## pre-commit
