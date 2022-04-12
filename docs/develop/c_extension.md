# C/C++ extensions

For Python.org docs over C/C++ extensions see
[this](https://docs.python.org/3/extending/extending.html){:target="\_blank"}.

For Cython explanation check out cython docs
[here](https://cython.readthedocs.io/en/latest/){:target="\_blank"}.
Building is described on
[this](https://cython.readthedocs.io/en/latest/){:target="\_blank"} page.

# GoogleTest

-   [Documentation for GoogleTest](https://google.github.io/googletest/)
-   [Documentation for Git submodule](https://git-scm.com/docs/git-submodule)

To add GoogleTest to git repository (already done) use

```
git submodule add https://github.com/google/googletest external/googletest
```

To initialize git submodules use

```
git submodule update --init --recursive
```

To checkout specific version of GoogleTest use

```
cd external/googletest
git checkout release-1.11.0
```

# Building

In this project, building binary extensions to python is designed as a two
step process.

1. Building C++ code with [CMake](https://cmake.org/){:target="\_blank"}
   and [Ninja](https://ninja-build.org/){:target="\_blank"}.
   This process is completely automated with tox, so just enter the command
   below and you will end up with a static library built in the build folder
   containing all the code from `source/internal`. All configuration is done
   by altering `CMakeLists.txt` files in root of this repository and in source
   folder (possibly nested in folders).

    ```
    tox -e cmake
    ```

2. Building Python interface is more complex and doesn't require any interaction
   from developer (until something breaks). Interface for C++ extension
   contained in static library compiled in step 1 is described in interface.pyx
   file in `source/optmath/_internal`.

    File with `pyx` extension is first compiled into C++ source file with
    [Cython](https://cython.org/){:target="\_blank"},
    then into dynamic library by common C++ compiler.

!!! Note

    For the convenience of use, the interface.pyx
    file should be accompanied by an
    [interface.pyi](https://stackoverflow.com/questions/41734836/what-does-i-represent-in-python-pyi-extension){:target="\_blank"}
    file containing the binary extensions
    API description in form of Python-compatible syntax with type hints and comments.
