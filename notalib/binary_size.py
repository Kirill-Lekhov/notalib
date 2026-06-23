from typing import Literal, Union
from enum import Enum


class SizeUnit(Enum):
	BYTE = "B"
	KILOBYTE = "KB"
	MEGABYTE = "MB"
	GIGABYTE = "GB"
	TERABYTE = "TB"


class SizeBiUnit(Enum):
	BYTE = "B"
	KIBIBIT = "KiB"
	MEBIBIT = "MiB"
	GIBIBIT = "GiB"
	TEBIBIT = "TiB"


SizeHumanizationMode = Literal["auto", "auto_bi", "TB", "GB", "MB", "KB", "TiB", "GiB", "MiB", "KiB"]


class Size:
	__slots__ = "value", "unit"

	def __init__(self, value: float, unit: Union[SizeUnit, SizeBiUnit]) -> None:
		self.value = value
		self.unit = unit

	def __str__(self) -> str:
		return f"{self.value:.2f} {self.unit.value}"


class SizeHumanizer:
	"""
	Converts size (in bytes) to specified unit.
	"""
	mode: SizeHumanizationMode

	def __init__(self, mode: SizeHumanizationMode = "auto") -> None:
		self.mode = mode

	def humanize(self, value: float) -> Size:
		if self.mode == "auto":
			return self.to_auto(value)
		elif self.mode == "TB":
			return self.to_tb(value)
		elif self.mode == "GB":
			return self.to_gb(value)
		elif self.mode == "MB":
			return self.to_mb(value)
		elif self.mode == "KB":
			return self.to_kb(value)
		elif self.mode == "auto_bi":
			return self.to_auto_bi(value)
		elif self.mode == "TiB":
			return self.to_tib(value)
		elif self.mode == "GiB":
			return self.to_gib(value)
		elif self.mode == "MiB":
			return self.to_mib(value)
		elif self.mode == "KiB":
			return self.to_kib(value)

		raise NotImplementedError(f"Unexpected mode: {self.mode}")

	@staticmethod
	def convert_unit(value: float) -> float:
		return value / 1000

	@staticmethod
	def convert_unit_bi(value: float) -> float:
		return value / 1024

	@classmethod
	def to_auto(cls, value: float) -> Size:
		unit = SizeUnit.BYTE

		for new_unit in [SizeUnit.KILOBYTE, SizeUnit.MEGABYTE, SizeUnit.GIGABYTE, SizeUnit.TERABYTE]:
			if value < 1000:
				break

			value = cls.convert_unit(value)
			unit = new_unit

		return Size(value, unit)

	@classmethod
	def to_tb(cls, value: float) -> Size:
		return Size(cls.convert_unit(cls.to_gb(value).value), SizeUnit.TERABYTE)

	@classmethod
	def to_gb(cls, value: float) -> Size:
		return Size(cls.convert_unit(cls.to_mb(value).value), SizeUnit.GIGABYTE)

	@classmethod
	def to_mb(cls, value: float) -> Size:
		return Size(cls.convert_unit(cls.to_kb(value).value), SizeUnit.MEGABYTE)

	@classmethod
	def to_kb(cls, value: float) -> Size:
		return Size(cls.convert_unit(value), SizeUnit.KILOBYTE)

	@classmethod
	def to_auto_bi(cls, value: float) -> Size:
		unit = SizeBiUnit.BYTE

		for new_unit in [SizeBiUnit.KIBIBIT, SizeBiUnit.MEBIBIT, SizeBiUnit.GIBIBIT, SizeBiUnit.TEBIBIT]:
			if value < 1024:
				break

			value = cls.convert_unit_bi(value)
			unit = new_unit

		return Size(value, unit)

	@classmethod
	def to_tib(cls, value: float) -> Size:
		return Size(cls.convert_unit_bi(cls.to_gib(value).value), SizeBiUnit.TEBIBIT)

	@classmethod
	def to_gib(cls, value: float) -> Size:
		return Size(cls.convert_unit_bi(cls.to_mib(value).value), SizeBiUnit.GIBIBIT)

	@classmethod
	def to_mib(cls, value: float) -> Size:
		return Size(cls.convert_unit_bi(cls.to_kib(value).value), SizeBiUnit.MEBIBIT)

	@classmethod
	def to_kib(cls, value: float) -> Size:
		return Size(cls.convert_unit_bi(value), SizeBiUnit.KIBIBIT)
