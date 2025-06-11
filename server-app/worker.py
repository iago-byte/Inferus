from __future__ import annotations

"""Simple background task worker using :mod:`concurrent.futures`."""

from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Dict, Any
import uuid

# Executor used for running background tasks. 4 workers by default.
_executor = ThreadPoolExecutor(max_workers=4)
# Mapping from task id to future for status inspection
_tasks: Dict[str, Future] = {}

def submit(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """Submit ``func`` to be executed in a worker thread.

    Returns the generated task id that can be used to query the status.
    """
    task_id = str(uuid.uuid4())
    future = _executor.submit(func, *args, **kwargs)
    _tasks[task_id] = future
    return task_id

def status(task_id: str) -> Dict[str, Any]:
    """Return the current status of the given ``task_id``."""
    fut = _tasks.get(task_id)
    if fut is None:
        return {"status": "not_found"}
    if fut.done():
        if fut.exception() is not None:
            return {"status": "failed", "error": str(fut.exception())}
        return {"status": "completed", "result": fut.result()}
    return {"status": "running"}

def shutdown() -> None:
    """Shut down the worker pool."""
    _executor.shutdown(wait=False)