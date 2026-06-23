from notalib.table import number_to_letters

import pytest


class TestNumberToLetters:
	@pytest.mark.parametrize(
		"num, expected_result",
		[
			(1, "A"),
			(2, "B"),
			(33, "AG"),
			(123, "DS"),
		]
	)
	def test_normal(self, num: int, expected_result: str):
		assert number_to_letters(num) == expected_result

	def test_error(self):
		with pytest.raises(TypeError, match="Number must be of int type"):
			number_to_letters(1.1)		# type: ignore - for testing purposes
