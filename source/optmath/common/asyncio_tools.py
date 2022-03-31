"""AsyncIO common utilities."""

import asyncio
from typing import Any, Coroutine


def await_async(task: Coroutine[Any, Any, Any]) -> Any:
    """Await async task in sync function.

    Parameters
    ----------
    task : Coroutine
        task to be awaited, eg f() where f is async function.

    Returns
    -------
    Any
        Result returned from awaited task.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(task)
