from .filterset import create_filter_set, from_request

import pytest
from django.forms import IntegerField, CharField


def test_filter_set():
	CountryFilterSet = create_filter_set({
		'country': CharField(required=True),
	}, required=['country'])

	AddressFilterSet = create_filter_set({
		'city': CharField(required=True),
		'street': CharField(),
		'building': IntegerField(),
	}, required=['city'], parent=CountryFilterSet)

	with pytest.raises(AssertionError):
		from_request(AddressFilterSet, {})

	with pytest.raises(AssertionError):
		from_request(AddressFilterSet, {
			'country': 'Russia',
		})

	source = {
		'country': 'Russia',
		'city': 'Penza',
		'street': 'Hi st.',
		'building': '344',
	}
	expected = {
		'country': 'Russia',
		'city': 'Penza',
		'street': 'Hi st.',
		'building': 344,
	}
	r = from_request(AddressFilterSet, source)
	assert r.is_valid
	r.data.unfreeze(['country', 'city', 'street', 'building'])
	assert r.data.as_dict() == expected

	AddressFilterSet = create_filter_set({
		'city': CharField(required=True),
		'building': IntegerField(required=True, min_value=0),
		'street': CharField(),
	}, required=['city'], parent=CountryFilterSet)

	r = from_request(AddressFilterSet, {
		'country': 'Russia',
		'city': 'Penza',
		'building': 344,
	})

	assert not r.is_valid
	assert r.data is None
	assert len(r.errors) == 1
