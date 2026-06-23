from string import ascii_uppercase


def number_to_letters(number: int) -> str:
	"""
	Converts number to collection of letters (excel-like representation).

	Examples:
		>>> number_to_letters(1)		# "A"
		>>> number_to_letters(33)		# "AG"
	"""
	if not isinstance(number, int):
		raise TypeError("Number must be of int type")

	result = []
	letter_count = len(ascii_uppercase)

	while number:
		number, rem = divmod(number - 1, letter_count)
		result.insert(0, ascii_uppercase[rem])

	return "".join(result)
