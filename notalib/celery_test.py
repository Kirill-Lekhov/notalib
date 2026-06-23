from .celery import is_task_running, wait_complete

from unittest.mock import patch, Mock
from logging import DEBUG

import pytest


def test_is_task_running():
	with patch("notalib.celery.current_app.control.inspect") as inspect_mock:
		inspect_mock.return_value = Mock()
		inspect_mock.return_value.active.return_value = {}
		assert not is_task_running("task")

		inspect_mock.return_value.active.return_value = {1: [], 2: [], 3: []}
		assert not is_task_running("task")

		inspect_mock.return_value.active.return_value = {
			1: [
				{"name": "a"},
				{"name": "b"},
				{"name": "c"},
			],
			2: [
				{"name": "d"},
				{"name": "e"},
				{"name": "f"},
			],
			3: [
				{"name": "task"},
			],
		}
		assert is_task_running("task")


class TestWaitComplete:
	def test_normal(self, caplog):
		caplog.set_level(DEBUG)

		with patch("notalib.celery.is_task_running") as is_task_running_mock:
			with patch("notalib.celery.sleep") as sleep_mock:
				is_task_running_mock.side_effect = [True, True, True, False]
				sleep_mock.return_value = None
				wait_complete("task", 5)

				assert sleep_mock.call_count == 3

		assert len(caplog.records) == 3

		for record in caplog.records:
			assert record.levelname == "DEBUG"
			assert record.message == "The task 'task' is steel running. Next check after 5s"

	def test_error(self):
		with pytest.raises(ValueError, match="The 'timeout' must be greater than or equal to zero"):
			wait_complete("task", -100)
