from enum import Enum
from time import sleep
from logging import getLogger; log = getLogger(__name__)

from celery import current_app


def is_task_running(name: str) -> bool:
	"""
	Checks whether a task is running.

	Args:
		name: Celery task name (e.g. 'main.tasks.my_task').

	Returns:
		True if specified task is running otherwise False.
	"""
	inspect = current_app.control.inspect()

	if active_tasks := inspect.active():
		for tasks in active_tasks.values():
			for task in tasks:
				if task["name"] == name:
					return True

	return False


def wait_complete(name: str, timeout: float = 5) -> None:
	"""
	Waits for a celery task to complete.

	Args:
		name: Celery task name (e.g. 'main.tasks.my_task').
		timeout: (in seconds) Timeout between attempts to check the status of a task.
	"""
	if timeout < 0:
		raise ValueError("The 'timeout' must be greater than or equal to zero")

	while is_task_running(name):
		log.debug(f"The task '{name}' is steel running. Next check after {timeout}s")
		sleep(timeout)


class TaskStatus(Enum):
	"""
	Enumeration of celery task status.

	Actual for celery 5.3.6.
	"""
	PENDING = "PENDING"
	RECEIVED = "RECEIVED"
	STARTED = "STARTED"
	SUCCESS = "SUCCESS"
	FAILURE = "FAILURE"
	REVOKED = "REVOKED"
	REJECTED = "REJECTED"
	RETRY = "RETRY"
	IGNORED = "IGNORED"
