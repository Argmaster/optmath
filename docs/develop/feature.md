# Feature flow

This project uses
**[GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow){:target="\_blank"}**
as it's main workflow model. Simplified visualization can be seen on graph
below:

```mermaid
graph LR
  A(master) --> B((branch));
  B -->|master| Z((merge));
  B --> C([commits]);
  C --> E((Pull Request));
  E --> G([test, fix, discuss]);
  G --> Z;
  Z --> X(master);
```

## Clone repository

!!! info "you can skip this step if you already have a clone"

!!! Tip "[How to clone git repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository){:target="\_blank"}"

```
git clone https://github.com/Argmaster/optmath.git
```

## Pull changes from origin

!!! info "You can skip this step if you just cloned the repository"

!!! Tip "[What is the difference between 'git pull' and 'git fetch'?](https://stackoverflow.com/questions/292357/what-is-the-difference-between-git-pull-and-git-fetch){:target="\_blank"}"

```
git pull
```

## Checking out main branch

Make sure we are on `main` branch.

    ```
    git checkout main
    ```

## Create feature branch

Create new branch for our feature called `feature_name`. `feature/` prefix
is not required but is recommended to distinguish features from fixes and
other types of branches in git history.

[Learn about branches](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging){:target="\_blank"}

```
git checkout -b feature/feature_name
```

## Check repository status

```
git status
```

Result should be similar to this:

```
On branch feature/feature_name
nothing to commit, working tree clean
```

## Test-commit-push cycle

Your work on a feature should be divided into many steps during
which you will add new units to the system. Each unit should
have a set of tests to verify its operation.

### 1. Formatting & Quality checks

Run code quality checks with tox to quickly fix most obvious issues in your code.

```
tox -e check
```

### 2. Run test suite for Python interpreter versions you have locally

!!! tip "[More about tox](/develop/tox_basics/){:target="\_blank"}"

First build C/C++ extensions with

```
tox -e cmake
```

Then run test suites on available interpreters with

```
tox -e py37
```

!!! tip "[Tox pyXX environments](/develop/tox_basics/#pyxx){:target="\_blank"}"

!!! danger "Important"

    If the tests fail, you have to repeat steps 1 and 2. Omission of the
    corrections will result in your changes being rejected by the CI
    tests executed for the pull request

### 3. Add all changes to staging area with

```
git add *
```

!!! tip

    You can list file paths instead of using the asterisk symbol if you know
    you can add many unwanted files. If these unwanted files regularly appear
    in the codebase, add them to the `.gitignore` file.

### Check staging area

```
git status
```

!!! tip

    If any files staged for commit shouldn't be there, unstage them with

    ```
    git restore --staged <file>
    ```

### 4. Commit changes to git history with

!!! tip

    You can use

    ```
    git commit -m "commit message"
    ```

    to add commit title and omit long description

!!! tip

    The commit title should not be longer than 50 characters.

    - [How to write a Git Commit Message](https://cbea.ms/git-commit/){:target="\_blank"}
    - [Good Commit Messages: A Practical Git Guide](https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/){:target="\_blank"}

```
git commit
```

### 6. Push changes to remote branch

    ```
    git push -u origin feature/feature_name
    ```

!!! tip

    For each subsequent push from this branch, you can omit `-u origin feature/feature_name`

    ```
    git push
    ```

## Create pull request

Visit [pull requests](https://github.com/Argmaster/optmath/pulls){:target="\_blank"}
and create PR for you feature.
