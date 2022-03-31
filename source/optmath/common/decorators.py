"""Custom decorators commonly used in project."""

import warnings
from dataclasses import dataclass
from datetime import datetime
from types import SimpleNamespace
from typing import Any, Dict, Optional, Type

import optmath
from packaging.version import Version


def statefull(**self_kwargs: Any):
    """Make function statefull.

    Statefull function will receive same namespace object
    as first argument every call. Namespace object will
    contain all attributes passed to statefull() call
    and can be modified. Modification will be persistent
    between calls.

    self object always contains following fields:
    - __function__ - described function object
    - __wrapper__ - wrapper object
    - __self_kwargs__ - bound kwargs as dict

    statefull have to be always called when used as descriptor.
    even when no args & kwargs are bound: @statefull()
    """

    def descriptor(function: Any):
        def wrapper(*args: Any, **kwargs: Any):
            return self.__function__(
                self,
                *args,
                **kwargs,
            )

        self = SimpleNamespace(**self_kwargs)
        self.__function__ = function
        self.__wrapper__ = wrapper
        self.__self_kwargs__ = self_kwargs

        return wrapper

    return descriptor


def ignore_excess_kwargs(cls: Any):
    """Make dataclass ignore excess keyword arguments. It will trim positional
    arguments too, but won't take into account the keyword arguments count.

    Use this decorator AFTER @dataclass.
    ```
    @ignore_excess_kwargs
    @dataclass
    class A:
        a: int
        b: str
    ```

    By default dataclasses doesn't accept keword arguments
    and will raise exception when excess kwargs are passed
    to their constructor. This decorator suppresses this
    behavior. Usefull for automatic REST API response
    to-class dispatching.

    Returns
    -------
    type
        dataclass to wrap
    """
    assert hasattr(cls, "__dataclass_fields__"), "Class has to be a dataclass."

    __old_init__ = cls.__init__

    def wrapper_init(self: Any, *args: Any, **kwargs: Any):
        fields: Dict[str, type] = cls.__dataclass_fields__
        max_args = len(fields)
        selected_kwargs = {
            k: kwargs.pop(k) for k in fields.keys() & kwargs.keys()
        }
        trimmed_args = args[: max_args - len(selected_kwargs)]
        __old_init__(
            self,
            *trimmed_args,
            **selected_kwargs,
        )

    cls.__init__ = wrapper_init
    return cls


class DeprecatedError(Exception):
    """Raised in deprecation bomb."""

    pass


@dataclass
class Bomb:
    functionality: str

    def __call__(self, *_: Any, **__: Any) -> Any:
        raise DeprecatedError(
            f"{self.functionality} is deprecated and no longer can be used."
        )


@dataclass
class deprecated:  # noqa: N801
    """Mark callable deprecated.

    Causes deprecation message to appear when object is called.
    To work properly, deprecated have to be called while used as
    descriptor, even if no parameters are given: @deprecated()

    Parameters
    ----------
    message_or_function : Union[str, Callable, None], optional
        message to display, None will result in default message being used.
    warning_type : object, optional
        type of warning object, by default FutureWarning
    date_bomb : datetime, optional
        creates a datetime bomb: callable will raise Exception after
        specified datetime.
    version_bomb: str, optional
        creates a version bomb: callable will raise Exception after
        specified version.

    Returns
    -------
    Any
        forwarded function return value.

    Raises
    ------
    TypeError
        raised when message_or_function is neither str or callable.
    """

    message: Optional[str] = None
    warning_type: Type[Warning] = FutureWarning
    date_bomb: Optional[datetime] = None
    version_bomb: Optional[str] = None

    def __call__(self, function: ...) -> ...:
        """Decorate function by replacing with wrapper."""
        should_bomb_trigger = (
            self.date_bomb is not None and datetime.now() > self.date_bomb
        ) or (
            self.version_bomb is not None
            and Version(optmath.__version__) > Version(self.version_bomb)
        )
        if should_bomb_trigger:
            return Bomb(f"{function.__module__}.{function.__qualname__}")

        else:
            message = (
                f"Function {function.__module__}.{function.__qualname__}"
                " was marked deprecated and soon will be removed, "
                "change your code so it won't break after update."
            )

            def function_wrapper(*args: Any, **kwargs: Any):
                warnings.warn(
                    self.warning_type(message),
                    category=self.warning_type,
                    stacklevel=2,
                )
                return function(*args, **kwargs)

            return function_wrapper
