from .channels import send_message_to_group, send_worker_task

from unittest.mock import patch, AsyncMock
from asyncio import run


def test_send_message_to_group():
	with patch("notalib.django.channels.get_channel_layer") as get_channel_layer_mock:
		get_channel_layer_mock.return_value = AsyncMock()
		get_channel_layer_mock.return_value.group_send.return_value = None

		run(send_message_to_group("GROUP", {"key": "value"}))
		get_channel_layer_mock.return_value.group_send.assert_called_once_with("GROUP", {"key": "value"})


def test_send_worker_task():
	with patch("notalib.django.channels.get_channel_layer") as get_channel_layer_mock:
		get_channel_layer_mock.return_value = AsyncMock()
		get_channel_layer_mock.return_value.send.return_value = None

		run(send_worker_task("WORKER", {"key": "value"}))
		get_channel_layer_mock.return_value.send.assert_called_once_with("WORKER", {"key": "value"})
