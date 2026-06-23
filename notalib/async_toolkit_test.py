from .async_toolkit import is_async_generator

from typing import Generator, AsyncGenerator


def test_is_async_generator():
	def count() -> int:
		return 0

	async def acount() -> int:
		return 0

	def get_numbers() -> Generator[int, None, None]:
		for i in range(10):
			yield i

	async def aget_numbers() -> AsyncGenerator[int, None]:
		for i in range(10):
			yield i


	class ORM:
		def count(self) -> int:
			return 0

		async def acount(self) -> int:
			return 0

		def get_numbers(self) -> Generator[int, None, None]:
			for i in range(10):
				yield i

		async def aget_numbers(self) -> AsyncGenerator[int, None]:
			for i in range(10):
				yield i


	assert not is_async_generator(count)
	assert not is_async_generator(acount)
	assert not is_async_generator(get_numbers)
	assert not is_async_generator(ORM.count)
	assert not is_async_generator(ORM.acount)
	assert not is_async_generator(ORM.get_numbers)
	assert is_async_generator(aget_numbers)
	assert is_async_generator(ORM.aget_numbers)
