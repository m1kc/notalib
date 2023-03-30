from typing import Sequence, Optional, Union, Any, List, Hashable, Dict, Callable
from itertools import compress
from operator import itemgetter
from copy import copy

from tablib import Dataset
from tablib.core import Row
from tablib.exceptions import HeadersNeeded, InvalidDimensions


class ExtendedDataset(Dataset):
	def drop_duplicates(self, subset: Optional[Union[str, Sequence]] = None) -> None:
		"""
		Removes all duplicate rows from the :class:`ExtendedDataset` object while maintaining the original order.

		Args:
			subset: Only consider certain columns for identifying duplicates, by default use all of the columns.

		Returns:
			This is inplace operation.
		"""
		seen = set()

		if subset is None:
			self.remove_duplicates()

		elif isinstance(subset, str):
			header_index = self.get_header_index(subset)
			self._data[:] = [row for row in self._data if not (row[header_index] in seen or seen.add(row[header_index]))]

		elif isinstance(subset, Sequence):
			headers_map = self.get_headers_map(subset)
			_data = []

			# TODO: It is possible to reduce memory consumption by using while
			for row in self._data:
				unique_data = tuple(compress(row, headers_map))

				if unique_data not in seen:
					seen.add(unique_data)
					_data.append(row)

			self._data[:] = _data

		else:
			raise TypeError("Unsupported subset type")

	def drop_empty(self, subset: Optional[Union[str, Sequence]] = None, empty_value: Optional[Any] = None) -> None:
		"""
		Removes rows with empty data in specified columns.

		Args:
			subset: Optional[Union[str, Sequence]]
				If it's None:
					All rows will be deleted all values in which are empty.
				If it's of str type:
					The rows whose values are empty in the specified column will be deleted.
				If it's of Sequence type:
					The rows whose values are empty in the specified column's will be deleted.
			empty_value: The value considered empty.

		Returns:
			This is inplace operation.
		"""
		if subset is None:
			self.drop_empty_rows(empty_value)

		elif isinstance(subset, str):
			header_index = self.get_header_index(subset)
			self._data[:] = [row for row in self._data if row[header_index] != empty_value]

		elif isinstance(subset, Sequence):
			headers_map = self.get_headers_map(subset)

			_data = []

			# TODO: It is possible to reduce memory consumption by using while
			for row in self._data:
				to_check = compress(row, headers_map)

				if all(map(lambda x: x != empty_value, to_check)):
					_data.append(row)

			self._data[:] = _data

		else:
			raise TypeError("Unsupported subset type")

	def drop_empty_rows(self, empty_value: Optional[Any] = None) -> None:
		"""
		Removes rows in which all values are empty.
		"""
		self._data[:] = [row for row in self._data if not all(map(lambda x: x == empty_value, row))]

	def apply_to_column(self, header_label: str, func: Callable, *args, **kwargs) -> None:
		"""
		Applies the function to the values in the specified column.

		Args:
			header_label: Column name.
			func: Function to be applied.
			args: Additional arguments of the function to be applied to the column values.
			kwargs: Additional named arguments of the function to be applied to the column values.

		Returns:
			This is inplace operation.
		"""
		column_number = self.get_header_index(header_label)

		def apply_func(col_num: int, val: Any) -> Any:
			if column_number == col_num:
				return func(val, *args, **kwargs)

			return val

		self._data[:] = [Row(apply_func(i, j) for i, j in enumerate(row)) for row in self._data]

	def replace_empty_objects(self, empty_value: Optional[Any] = None, new_value: Optional[Any] = None):
		"""
		Replaces empty values with a new one.
		"""
		self._data[:] = [Row(map(lambda x: new_value if x == empty_value else x, row)) for row in self._data]

	def set_used_columns(self, header_labels: Sequence[str]) -> 'ExtendedDataset':
		"""
		Returns a new dataset based on the specified header labels.

		Notes:
			Labels order matters.
		"""
		header_indexes = [self.get_header_index(header_label) for header_label in header_labels]
		_dataset = ExtendedDataset(headers=header_labels)

		# TODO: It is possible to reduce memory consumption by using while
		for i in self._data:
			_dataset.append(Row((i[k] for k in header_indexes)))

		return _dataset

	def get_headers_map(self, header_labels: Sequence) -> List[bool]:
		"""
		Returns a list of Boolean objects based on a given set of header labels.

		Useful for sampling data by specified columns.
		"""
		header_indexes = [self.get_header_index(i) for i in header_labels]
		header_map = [i in header_indexes for i in range(self.width)]

		return header_map

	def get_header_index(self, header_label: str) -> int:
		"""
		Calculates the index of the header by its label.
		"""
		if header_label not in self.headers:
			raise ValueError(f"Header with label '{header_label}' doesn't exist")

		return self.headers.index(header_label)

	def groupby(self, header_label: str) -> List[Hashable]:
		"""
		Sets tags to rows and returns list of groups for filtering.
		"""
		assert isinstance(header_label, str), "header_label must be of str type"
		header_index = self.get_header_index(header_label)
		groups = set()

		for row in self._data:
			group = row[header_index]
			row.tags = [group]
			groups.add(group)

		return list(groups)

	def rename_headers(self, rename_rules: Dict[str, str]) -> None:
		"""
		Renames header labels.

		Args:
			rename_rules: Contains the old name as the key and the new name as the value.

		Returns:
			This is inplace operation.
		"""
		assert isinstance(rename_rules, dict), "rename_rules must be of dict type"

		self.headers[:] = [rename_rules.get(header, header) for header in self.headers]

	##########################################################################################
	# Parent methods in which only the type is replaced                                      #
	# -------------------------------------------------------------------------------------- #
	# By default, the parent class returns an object of the Dataset class from these methods #
	# therefore, these methods have been modified to return objects of ExtendedDataset class #
	##########################################################################################
	def sort(self, col, reverse=False):
		"""Sort a :class:`ExtendedDataset` by a specific column, given string (for
		header) or integer (for column index). The order can be reversed by
		setting ``reverse`` to ``True``.

		Returns a new :class:`ExtendedDataset` instance where columns have been
		sorted.
		"""

		if isinstance(col, str):

			if not self.headers:
				raise HeadersNeeded

			_sorted = sorted(self.dict, key=itemgetter(col), reverse=reverse)
			_dset = ExtendedDataset(headers=self.headers, title=self.title)

			for item in _sorted:
				row = [item[key] for key in self.headers]
				_dset.append(row=row)

		else:
			if self.headers:
				col = self.headers[col]

			_sorted = sorted(self.dict, key=itemgetter(col), reverse=reverse)
			_dset = ExtendedDataset(headers=self.headers, title=self.title)

			for item in _sorted:
				if self.headers:
					row = [item[key] for key in self.headers]
				else:
					row = item
				_dset.append(row=row)

		return _dset

	def transpose(self):
		"""Transpose a :class:`ExtendedDataset`, turning rows into columns and vice
		versa, returning a new ``ExtendedDataset`` instance. The first row of the
		original instance becomes the new header row."""

		# Don't transpose if there is no data
		if not self:
			return

		_dset = ExtendedDataset()
		# The first element of the headers stays in the headers,
		# it is our "hinge" on which we rotate the data
		new_headers = [self.headers[0]] + self[self.headers[0]]

		_dset.headers = new_headers
		for index, column in enumerate(self.headers):

			if column == self.headers[0]:
				# It's in the headers, so skip it
				continue

			# Adding the column name as now they're a regular column
			# Use `get_col(index)` in case there are repeated values
			row_data = [column] + self.get_col(index)
			row_data = Row(row_data)
			_dset.append(row=row_data)
		return _dset

	def stack(self, other):
		"""Stack two :class:`ExtendedDataset` or :class:`Dataset` instances together by
		joining at the row level, and return new combined
		``ExtendedDataset`` instance."""

		if not (isinstance(other, Dataset) or isinstance(other, ExtendedDataset)):
			return

		if self.width != other.width:
			raise InvalidDimensions

		# Copy the source data
		_dset = copy(self)

		rows_to_stack = [row for row in _dset._data]
		other_rows = [row for row in other._data]

		rows_to_stack.extend(other_rows)
		_dset._data = rows_to_stack

		return _dset

	def stack_cols(self, other):
		"""Stack two :class:`ExtendedDataset` or :class:`Dataset` instances together by
		joining at the column level, and return a new
		combined ``ExtendedDataset`` instance. If either dataset
		has headers set, than the other must as well."""

		if not (isinstance(other, Dataset) or isinstance(other, ExtendedDataset)):
			return

		if self.headers or other.headers:
			if not self.headers or not other.headers:
				raise HeadersNeeded

		if self.height != other.height:
			raise InvalidDimensions

		try:
			new_headers = self.headers + other.headers
		except TypeError:
			new_headers = None

		_dset = ExtendedDataset()

		for column in self.headers:
			_dset.append_col(col=self[column])

		for column in other.headers:
			_dset.append_col(col=other[column])

		_dset.headers = new_headers

		return _dset

	def subset(self, rows=None, cols=None):
		"""Returns a new instance of the :class:`ExtendedDataset`,
		including only specified rows and columns.
		"""

		# Don't return if no data
		if not self:
			return

		if rows is None:
			rows = list(range(self.height))

		if cols is None:
			cols = list(self.headers)

		# filter out impossible rows and columns
		rows = [row for row in rows if row in range(self.height)]
		cols = [header for header in cols if header in self.headers]

		_dset = ExtendedDataset()

		# filtering rows and columns
		_dset.headers = list(cols)

		_dset._data = []
		for row_no, row in enumerate(self._data):
			data_row = []
			for key in _dset.headers:
				if key in self.headers:
					pos = self.headers.index(key)
					data_row.append(row[pos])
				else:
					raise KeyError

			if row_no in rows:
				_dset.append(row=Row(data_row))

		return _dset
