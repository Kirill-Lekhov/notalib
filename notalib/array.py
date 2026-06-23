from typing import Iterable, TypeVar, Generator, Tuple, AsyncIterable, AsyncGenerator
from itertools import islice


T = TypeVar('T')


def as_chunks(arr, n):
	"""
	Yield successive n-sized chunks from arr.
	"""
	assert n >= 1
	for i in range(0, len(arr), n):
		yield arr[i:i + n]


def ensure_iterable(x):
	if isinstance(x, list): return x
	if isinstance(x, tuple): return x
	# TODO other cases
	return (x,)


def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
	"""
	Batch data from the iterable into tuples of length n.

	Args:
		iterable: An iterable to batch.
		n: Batch size.

	Notes:
		* Src: https://docs.python.org/3.12/library/itertools.html#itertools.batched
		* See `abatched` if you looking for async version.

	Examples:
		>>> list(batched('ABCDEFG', 3))
		... [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', )]
	"""
	if n < 1:
		raise ValueError('n must be at least one')

	it = iter(iterable)
	batch = tuple(islice(it, n))

	while batch:
		yield batch
		batch = tuple(islice(it, n))


async def abatched(iterable: AsyncIterable[T], batch_size: int) -> AsyncGenerator[Tuple[T, ...], None]:
	"""
	Divides an asynchronous iterable into equal parts of a given size.

	Args:
		iterable: An iterable to be divided.
		batch_size: Size of one batch.

	Note:
		* See `batched` if you looking for sync version.
	"""
	if batch_size < 1:
		raise ValueError("The batch_size cannot be less than 1")

	buffer = []

	async for i in iterable:
		buffer.append(i)

		if len(buffer) == batch_size:
			yield tuple(buffer)
			buffer.clear()

	if buffer:
		yield tuple(buffer)
