from .binary_size import Size, SizeHumanizer, SizeUnit, SizeBiUnit, SizeHumanizationMode

from unittest.mock import patch, Mock
from typing import List, Tuple

import pytest


class TestSize:
	def test___init__(self):
		size = Size(1.1, SizeUnit.MEGABYTE)
		assert size.value == 1.1
		assert size.unit is SizeUnit.MEGABYTE

	def test___str__(self):
		size = Size(1.1056, SizeUnit.MEGABYTE)
		assert size.__str__() == "1.11 MB"


class TestSizeHumanizer:
	def test___init__(self):
		assert SizeHumanizer().mode == "auto"
		assert SizeHumanizer("GB").mode == "GB"

	def test_humanize(self):
		modes_and_methods: List[Tuple[SizeHumanizationMode, str]] = [
			("auto", "to_auto"),
			("TB", "to_tb"),
			("GB", "to_gb"),
			("MB", "to_mb"),
			("KB", "to_kb"),
			("auto_bi", "to_auto_bi"),
			("TiB", "to_tib"),
			("GiB", "to_gib"),
			("MiB", "to_mib"),
			("KiB", "to_kib"),
		]

		for mode, method in modes_and_methods:
			method_mock = Mock()

			with patch.object(SizeHumanizer, method, method_mock):
				method_mock.return_value = "TEST"
				humanizer = SizeHumanizer(mode)
				assert humanizer.humanize(1.1) == "TEST"
				method_mock.assert_called_once_with(1.1)

		humanizer = SizeHumanizer("UNKNOWN")		# type: ignore - for testing purposes

		with pytest.raises(NotImplementedError, match="Unexpected mode: UNKNOWN"):
			humanizer.humanize(1.1)

	def test_convert_unit(self):
		assert SizeHumanizer.convert_unit(0) == 0
		assert SizeHumanizer.convert_unit(1000) == pytest.approx(1, 0.001)
		assert SizeHumanizer.convert_unit(2000) == pytest.approx(2, 0.001)

	def test_convert_unit_bi(self):
		assert SizeHumanizer.convert_unit_bi(0) == 0
		assert SizeHumanizer.convert_unit_bi(1024) == pytest.approx(1, 0.001)
		assert SizeHumanizer.convert_unit_bi(2048) == pytest.approx(2, 0.001)

	@pytest.mark.parametrize(
		"source_value, expected_size, expected_unit",
		[
			(999, 999, SizeUnit.BYTE),
			(1999, 1.999, SizeUnit.KILOBYTE),
			(1999999, 1.999999, SizeUnit.MEGABYTE),
			(1999999999, 1.999999999, SizeUnit.GIGABYTE),
			(1999999999999, 1.999999999999, SizeUnit.TERABYTE),
			(1999999999999999, 1999.999999999999, SizeUnit.TERABYTE),
		],
	)
	def test_to_auto(self, source_value, expected_size, expected_unit):
		size = SizeHumanizer.to_auto(source_value)
		assert size.value == pytest.approx(expected_size, 0.0001)
		assert size.unit is expected_unit

	def test_to_tb(self):
		size = SizeHumanizer.to_tb(999999999999)
		assert size.value == pytest.approx(0.999999999999, 0.001)
		assert size.unit is SizeUnit.TERABYTE

		size = SizeHumanizer.to_tb(1000000000000)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeUnit.TERABYTE

		size = SizeHumanizer.to_tb(10010000000000)
		assert size.value == pytest.approx(10.01, 0.01)
		assert size.unit is SizeUnit.TERABYTE

	def test_to_gb(self):
		size = SizeHumanizer.to_gb(999999999)
		assert size.value == pytest.approx(0.999999999, 0.001)
		assert size.unit is SizeUnit.GIGABYTE

		size = SizeHumanizer.to_gb(1000000000)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeUnit.GIGABYTE

		size = SizeHumanizer.to_gb(1001000000)
		assert size.value == pytest.approx(1.001, 0.001)
		assert size.unit is SizeUnit.GIGABYTE

	def test_to_mb(self):
		size = SizeHumanizer.to_mb(999999)
		assert size.value == pytest.approx(0.999999, 0.001)
		assert size.unit is SizeUnit.MEGABYTE

		size = SizeHumanizer.to_mb(1000000)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeUnit.MEGABYTE

		size = SizeHumanizer.to_mb(1001000)
		assert size.value == pytest.approx(1.001, 0.001)
		assert size.unit is SizeUnit.MEGABYTE

	def test_to_kb(self):
		size = SizeHumanizer.to_kb(999)
		assert size.value == pytest.approx(0.999, 0.001)
		assert size.unit is SizeUnit.KILOBYTE

		size = SizeHumanizer.to_kb(1000)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeUnit.KILOBYTE

		size = SizeHumanizer.to_kb(1001)
		assert size.value == pytest.approx(1.001, 0.001)
		assert size.unit is SizeUnit.KILOBYTE

	@pytest.mark.parametrize(
		"source_value, expected_size, expected_unit",
		[
			(1023, 1023, SizeBiUnit.BYTE),
			(2047, 1.999, SizeBiUnit.KIBIBIT),
			(1048576, 0.999999, SizeBiUnit.MEBIBIT),
			(1073741825, 0.999999999, SizeBiUnit.GIBIBIT),
			(1099511627777, 0.999999999999, SizeBiUnit.TEBIBIT),
			(1125899906842625, 1024, SizeBiUnit.TEBIBIT),
		],
	)
	def test_to_auto_bi(self, source_value, expected_size, expected_unit):
		size = SizeHumanizer.to_auto_bi(source_value)
		assert size.value == pytest.approx(expected_size, 0.0001)
		assert size.unit is expected_unit

	def test_to_tib(self):
		size = SizeHumanizer.to_tib(1099511627775)
		assert size.value == pytest.approx(0.999999999999, 0.001)
		assert size.unit is SizeBiUnit.TEBIBIT

		size = SizeHumanizer.to_tib(1099511627776)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeBiUnit.TEBIBIT

		size = SizeHumanizer.to_tib(11006111394038)
		assert size.value == pytest.approx(10.01, 0.01)
		assert size.unit is SizeBiUnit.TEBIBIT

	def test_to_gib(self):
		size = SizeHumanizer.to_gib(1073741823)
		assert size.value == pytest.approx(0.999999999, 0.001)
		assert size.unit is SizeBiUnit.GIBIBIT

		size = SizeHumanizer.to_gib(1073741824)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeBiUnit.GIBIBIT

		size = SizeHumanizer.to_gib(1084479242)
		assert size.value == pytest.approx(1.01, 0.01)
		assert size.unit is SizeBiUnit.GIBIBIT

	def test_to_mib(self):
		size = SizeHumanizer.to_mib(1048575)
		assert size.value == pytest.approx(0.999999999, 0.001)
		assert size.unit is SizeBiUnit.MEBIBIT

		size = SizeHumanizer.to_mib(1048576)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeBiUnit.MEBIBIT

		size = SizeHumanizer.to_mib(1059062)
		assert size.value == pytest.approx(1.01, 0.01)
		assert size.unit is SizeBiUnit.MEBIBIT

	def test_to_kib(self):
		size = SizeHumanizer.to_kib(1023)
		assert size.value == pytest.approx(0.999999999, 0.001)
		assert size.unit is SizeBiUnit.KIBIBIT

		size = SizeHumanizer.to_kib(1024)
		assert size.value == pytest.approx(1, 0)
		assert size.unit is SizeBiUnit.KIBIBIT

		size = SizeHumanizer.to_kib(1034)
		assert size.value == pytest.approx(1.01, 0.01)
		assert size.unit is SizeBiUnit.KIBIBIT
