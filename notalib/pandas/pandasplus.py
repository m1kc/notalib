from typing import Tuple, Hashable, Any, Optional

from pandas import DataFrame, notnull, Series


def row_to_dict(d: Tuple[Hashable, Series], key_as: Optional[Hashable] = None) -> dict:
	"""
	Converts row recieved from 'DataFrame.iterrows' iterator.

	Args:
		d: DataFrame row recieved from 'iterrows' iterator.
		key_as: If it is not None, then the row ID will be saved by this key.

	Examples:
		>>> df = DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
		>>> for row in df.iterrows():
		>>> 	print(row_to_dict(row))
		{'A': 1, 'B': 4}
		{'A': 2, 'B': 5}
		{'A': 3, 'B': 6}
	"""
	key, value = d
	# 'to_dict' method returns 'collections.abc.Mapping' object and it does not support assignment
	ret = dict(value.to_dict())

	if key_as is not None:
		ret[key_as] = key

	return ret


def replace_null_objects(dataframe: DataFrame, new_value: Any = None) -> DataFrame:
	"""
	Returns pandas DataFrame with changed (pd.NaT, pd.NaN and NULL) values to <new_value>.

	Args:
		dataframe: DataFrame
			Source dataframe in which will be changed all null values.
		new_value: Any | Default None
			New null value object.

	Returns:
		Pandas dataframe with replaced all null values to new_value.

	Notes:
		Sometimes (especially in older versions of pandas) it happens that when importing a file, columns are assigned
		types, and empty cells are converted to corresponding null types. To standardize the format of null values or
		change it to None, I recommend using this function.
	"""
	dataframe = dataframe.where(notnull(dataframe), new_value)

	return dataframe
