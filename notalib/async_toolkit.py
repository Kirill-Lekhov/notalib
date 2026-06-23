from typing import Callable, get_origin
from collections.abc import AsyncGenerator
from inspect import signature


def is_async_generator(callable: Callable) -> bool:
	"""
	Checks whether function is asynchronous generator.

	Note:
		* Tested only on functions that have a return data type specified.
	"""
	return get_origin(signature(callable).return_annotation) is AsyncGenerator
