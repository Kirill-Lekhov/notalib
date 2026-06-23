from channels.layers import get_channel_layer


async def send_message_to_group(group: str, message: dict) -> None:
	"""
	Sends message to specific group.

	Args:
		group: Label of the group to send the message to.
		message: The message to send to the group.
	"""
	channel_layer = get_channel_layer()
	await channel_layer.group_send(group, message)


async def send_worker_task(worker: str, message: dict) -> None:
	"""
	Sends task message to specific worker.

	Args:
		worker: Name of the worker to send the message to.
		message: The message to send to the worker.
	"""
	channel_layer = get_channel_layer()
	await channel_layer.send(worker, message)
