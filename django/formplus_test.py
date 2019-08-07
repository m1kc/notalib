from pyutil.django.formplus import MonthArrayField

from collections import namedtuple

from django.core.exceptions import ValidationError
import pytest


def testMonthArrayField():
    TestCase = namedtuple('TestCase', ['input', 'output', 'valid'])
    data = [
        TestCase(input='2019-01', output=[(2019, 1)], valid=True),
        TestCase(input='1999-02', output=[(1999, 2)], valid=True),
        TestCase(input='2019-01|2019-02|1917-10', output=[(2019, 1), (2019, 2), (1917, 10)], valid=True),
        TestCase(input='2678', valid=False, output=None),
        TestCase(input='-01', valid=False, output=None),
        TestCase(input='2019-01|672643787878', valid=False, output=None),
        TestCase(input='2019-01|2099-01||||||||||||||||      ', valid=False, output=None),
        TestCase(input='2019-13', output=None, valid=False),
    ]

    for d in data:
        f = MonthArrayField()
        if d.valid:
            assert f.clean(d.input) == d.output
        else:
            with pytest.raises(ValidationError):
                f.clean(d.input)