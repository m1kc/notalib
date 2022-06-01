from pandas import DataFrame, notnull


def row_to_dict(d, key_as=None):
	key, value = d
	ret = value.to_dict()
	if key_as is not None:
		ret[key_as] = key
	return ret


def replace_null_objects(dataframe: DataFrame, new_value=None) -> DataFrame:
	"""
	Returns pandas DataFrame with changed (pd.NaT, pd.NaN and NULL) values to <new_value>

	Parameters
	----------
	dataframe: DataFrame
		Source dataframe in which will be changed all null values.
	new_value: Any | Default None
		New null value object.

	Returns
	-------
	DataFrame:
		Pandas dataframe with replaced all null values to new_value.

	Notes
	-----
	Sometimes (especially in older versions of pandas) it happens that when importing a file, columns are assigned
	types, and empty cells are converted to corresponding null types. To standardize the format of null values or change
	it to None, I recommend using this function.
	"""

	dataframe = dataframe.where(notnull(dataframe), new_value)

	return dataframe
