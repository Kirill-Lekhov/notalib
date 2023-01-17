from .array import ensure_iterable
from .deprecated import deprecated

import datetime
from typing import Union, NamedTuple, Tuple, List, Optional
from abc import ABC, abstractmethod
from enum import Enum, auto, unique

import arrow


DateLikeObject = Union[datetime.date, datetime.datetime, arrow.Arrow]
DateFormats = Union[str, List[str], Tuple[str]]		# TODO: Change possible types in ensure_iterable and DateFormats.


class Week(NamedTuple):
	week: int
	year: int

	def __str__(self) -> str:
		return f"{self.week} week of {self.year} year"


@unique
class WeekNumbering(Enum):
	"""
	Contains enumeration of available modes of week extraction.
	"""

	"""
	First day in week is: Monday
	First week number in year is: One
	First week is a week with: The first of Monday
	"""
	NORMAL = auto()

	"""
	First day in week is: Monday
	First week number in year: Zero
	First week is a week with: The first of January
	"""
	MATCH_YEAR = auto()


def parse_month(yyyy_mm: str) -> Tuple[int, int]:
	"""
	Parses string which contains month and year.
	Expected format: 'YYYY-M'

	Args:
		yyyy_mm: Year and month to be parsed.

	Returns:
		Tuple where the first value is year and the second is month.

	Raises:
		ValueError: When data could not be extracted.
	"""
	a = arrow.get(yyyy_mm, 'YYYY-M')
	return a.year, a.month


def parse_date(s: str, format_or_formats: DateFormats) -> arrow.Arrow:
	"""
	Tries to parse the date according to the specified format or formats.

	Args:
		s: Date to be parsed.
		format_or_formats: Possible format or formats for date parsing.

	Raises:
		ValueError: When date can't be parsed.

	Returns:
		arrow.Arrow object.
	"""
	for f in ensure_iterable(format_or_formats):
		try:
			return arrow.get(s, f)

		except ValueError:
			pass

	raise ValueError(f"Could not parse date `{s}` with any of the specified formats")


def normalize_date(
	s: Optional[str],
	input_formats: DateFormats,
	output_format: str,
	allow_empty: bool = True,
) -> Optional[str]:
	"""
	Converts date from one format to another.

	Args:
		s: Date to be converted.
		input_formats: Possible format or formats for date parsing.
		output_format: The format to convert the date to.
		allow_empty: Flag for resolving an empty date value.

	Returns:
		None if source date is None and empty date is allowed.
	"""
	if s is None and allow_empty:
		return None

	return parse_date(s, input_formats).format(output_format)


class WeekExtractor(ABC):
	@classmethod
	@abstractmethod
	def extract(cls, date_object: DateLikeObject) -> Week: ...


class MatchYearWeekExtractor(WeekExtractor):
	@classmethod
	def extract(cls, date_object: DateLikeObject) -> Week:
		"""
		Returns week number of specified date with year.
		First week of year is week with monday.
		Range of week numbers: 0..53.
		0 means that week refers to the last week of the previous year.
		"""
		return Week(int(date_object.strftime('%W')), date_object.year)


class NormalWeekExtractor(WeekExtractor):
	@classmethod
	def extract(cls, date_object: DateLikeObject) -> Week:
		"""
		Returns week number of specified date with year.
		First week of year is week with monday.
		Range of week numbers: 1..53.
		"""
		week = MatchYearWeekExtractor.extract(date_object)

		if week.week == 0:
			# Means that the week refers to the last week of the previous year
			week = MatchYearWeekExtractor.extract(datetime.date(date_object.year - 1, 12, 31))

		return week


@deprecated('notalib: current get_week behavior is considered buggy and will be changed in 2.0.')
def get_week(
	date_object: DateLikeObject,
	mode: WeekNumbering = WeekNumbering.NORMAL,
) -> Week:
	"""
	Extracts week from specified date.

	Args:
		date_object: Date like object. It must be compatible with 'datetime.date' object.
		mode: Mode of extraction week number. Available modes see in WeekNumbering.
	"""
	if not isinstance(mode, WeekNumbering):
		raise TypeError(f"The mode {mode} does not belong to the {WeekNumbering.__name__} enumeration")

	if mode == WeekNumbering.NORMAL:
		return NormalWeekExtractor.extract(date_object)
	elif mode == WeekNumbering.MATCH_YEAR:
		return MatchYearWeekExtractor.extract(date_object)

	raise NotImplementedError(f'Extraction week number in mode {mode.name} is not implemented')
