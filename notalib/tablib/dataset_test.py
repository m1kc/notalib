from .dataset import ExtendedDataset

from pytest import raises


def test_drop_duplicates():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])

	ds.append(('DUPLICATED_VALUE', 0, 0))
	ds.append(('DUPLICATED_VALUE', 1, 1))
	ds.append((2, 'DUPLICATED_VALUE', 'DUPLICATED_VALUE'))
	ds.append((3, 'DUPLICATED_VALUE', 'DUPLICATED_VALUE'))
	ds.append((4, 4, 4))

	ds.drop_duplicates()		# check that nothing changed
	assert ds[0] == ('DUPLICATED_VALUE', 0, 0) and ds[1] == ('DUPLICATED_VALUE', 1, 1)

	ds.drop_duplicates('A')
	assert ds[0] == ('DUPLICATED_VALUE', 0, 0) and ds[1] == (2, 'DUPLICATED_VALUE', 'DUPLICATED_VALUE')

	ds.drop_duplicates(['B', 'C'])
	assert ds[0] == ('DUPLICATED_VALUE', 0, 0) and ds[1] == (2, 'DUPLICATED_VALUE', 'DUPLICATED_VALUE') and ds.height == 3

	with raises(TypeError, match="Unsupported subset type"):
		ds.drop_duplicates(15)


def test_drop_empty():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])
	[ds.append((i, i, i)) for i in range(5)]
	ds[0] = [0, None, 0]
	ds[1] = ['', '', 1]
	ds[2] = [[], [], []]
	ds[3] = [3, '', 3]

	ds.drop_empty(empty_value=[])
	assert ds[1] == ('', '', 1) and ds[2] == (3, '', 3)

	ds.drop_empty('B')
	assert ds[0] == ('', '', 1) and ds[1] == (3, '', 3)

	ds.drop_empty(['A', 'B'], empty_value='')
	assert ds[0] == (4, 4, 4) and ds.height == 1

	with raises(TypeError, match="Unsupported subset type"):
		ds.drop_empty(15)


def test_drop_empty_rows():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])
	ds.append((None, None, None))
	ds.append(('', '', ''))
	ds.append(([], [], []))

	ds.drop_empty_rows()
	assert ds.height == 2 and ds[0] == ('', '', '') and ds[1] == ([], [], [])
	ds.drop_empty_rows('')
	assert ds.height == 1 and ds[0] == ([], [], [])
	ds.drop_empty_rows([])
	assert not ds.height


def test_apply_to_column():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])
	[ds.append([i, i, i]) for i in range(5)]

	ds.apply_to_column('A', lambda x, y: x+y, 1)
	ds.apply_to_column('B', str)

	assert ds.get_col(0) == list(range(1, 6))
	assert ''.join(ds.get_col(1)) == '01234'
	assert ds.get_col(2) == list(range(5))


def test_replace_empty_objects():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])
	[ds.append([i, i, i]) for i in range(5)]
	ds[2] = (None, None, None)

	ds.replace_empty_objects(None, '')
	assert ds[2] == ('', '', '')

	ds.replace_empty_objects('', [])
	assert ds[2] == ([], [], [])

	ds.replace_empty_objects([], 'NOT EMPTY VALUE')
	assert ds[2] == ('NOT EMPTY VALUE', 'NOT EMPTY VALUE', 'NOT EMPTY VALUE')


def test_set_used_columns():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])

	assert ds.set_used_columns(['A', 'B']).headers == ['A', 'B']
	assert ds.set_used_columns(['B', 'A', 'C']).headers == ['B', 'A', 'C']
	assert ds.set_used_columns(['C']).headers == ['C']

	ds.append((1, 2, 3))
	ds.append((1, 2, 3))
	assert ds.set_used_columns(['A', 'B'])[0] == (1, 2)
	assert ds.set_used_columns(['B', 'A', 'C'])[0] == (2, 1, 3)
	assert ds.set_used_columns(['C'])[0] == (3, )


def test_get_headers_map():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])

	assert [False, False, False], ds.get_headers_map([])
	assert [True, True, False], ds.get_headers_map(['A', 'B'])
	assert [True, False, False], ds.get_headers_map(['A'])
	assert [True, True, True], ds.get_headers_map(['A', 'B', 'C'])
	assert [True, False, True], ds.get_headers_map(['C', 'A'])


def test_get_header_index():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])

	with raises(ValueError, match="Header with label 'D' doesn't exist"):
		ds.get_header_index('D')

	assert list(range(3)) == [ds.get_header_index(i) for i in 'ABC']


def test_groupby():
	ds = ExtendedDataset(
		('Hello', 'World', '!'),
		('Hello', 'Russia', '!'),
		('Comearth', 'Russia', ''),
		headers=['A', 'B', 'C']
	)

	with raises(AssertionError, match="header_label must be of str type"):
		groups = ds.groupby(11)

	groups = sorted(ds.groupby('A'))
	assert groups == ['Comearth', 'Hello']
	assert ds.filter('Hello')[0] == ('Hello', 'World', '!')
	assert ds.filter('Comearth')[0] == ('Comearth', 'Russia', '')


def test_rename_headers():
	ds = ExtendedDataset(headers=['A', 'B', 'C'])

	with raises(AssertionError, match="rename_rules must be of dict type"):
		ds.rename_headers('Wrong Argument')

	ds.rename_headers({'A': 'C', 'B': 'B', 'C': 'A'})
	assert ''.join(ds.headers) == 'CBA'
