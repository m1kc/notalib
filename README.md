# notalib [![Build Status](https://travis-ci.com/m1kc/notalib.svg?branch=master)](https://travis-ci.com/m1kc/notalib) [![Coverage Status](https://coveralls.io/repos/github/m1kc/notalib/badge.svg?branch=master)](https://coveralls.io/github/m1kc/notalib?branch=master)

Collection of small Python utility functions and classes. Some are written by me, some are taken from StackOverflow and customized (I tried to provide links to original sources where possible). This repo never aimed to be a library of any sort (but now it is).

## Install

```sh
pip install notalib
```

Or with [poetry](https://python-poetry.org/):

```sh
poetry add notalib
```

## Utils included

#### notalib.array.as_chunks :fire:

Iterates over your array in chunks of at most N elements.

```python
from notalib.array import as_chunks

arr = [1,2,3,4,5]
for chunk in as_chunks(arr, 2):
    print(chunk)
# [1,2]
# [3,4]
# [5]
```

#### notalib.array.ensure_iterable :fire:

Keeps iterable things like lists intact, turns single values into single-element lists. Useful for functions that can accept both.

```python
ensure_iterable([1,2,3])  # --> [1,2,3]
ensure_iterable((1,2,3))  # --> (1,2,3)
ensure_iterable(1)        # --> [1]
ensure_iterable('smth')   # --> ['smth']

def my_function(one_or_multiple_args):
    for arg in ensure_iterable(one_or_multiple_args):
        ...
        
my_function(['log', 'smog'])
my_function('dog')
```

#### notalib.combinator.Combinator :fire:
#### notalib.date.parse_month
#### notalib.date.parse_date
#### notalib.date.normalize_date :fire:
#### notalib.dict.find_field
#### notalib.dict.find_value
#### notalib.dict.normalize_dict :fire:
#### notalib.format.format_long_list
#### notalib.hypertext.strip_tags :fire:
#### notalib.hypertext.TablePrinter :fire:
#### notalib.polosa.polosa :fire: :fire: :fire: :fire: :fire:

```
18023/2000000   294.8/sec   Processing transaction ID#84378473 (2020-01-04)
```

The CLI progress indicator you've always dreamt of: shows current and total if available, measures current speed, can show your comments for each element, makes sure not to slow down your terminal with frequent updates. [See this short demo](https://asciinema.org/a/UI1aOqjQC1KXx303kaVGrxjQp).

_Cheat sheet_

```python
## Basic usage
with polosa() as p:
    p.tick()
# 467344   201.2/sec

## Specify total number of elements:
with polosa(total=1337) as p:
# 26/1337   1.2/sec

## Print something useful about every element:
p.tick(caption=my_order.time_created)
# 1723910/2000000   319231.2/sec   2020-01-01 15:37:00
```

#### notalib.range.Range
#### notalib.time.Timing :fire:

Measures time spent on executing your code. Killer feature: it can be used as a reusable context.

```python
timing = Timing()
...
with timing:
    do_something()
# That's it, do something with the measurement
log(f'Operation took {timing.result} sec')
```

If you just want to print measurements into console, there's a shorthand:

```python
timing = Timing(auto_print=True)
...
with timing:
    do_something()
```

#### notalib.trendsetter.Trendsetter :fire:

## Pandas-related

#### notalib.pandas.pandasplus.row_to_dict

## Django-related

#### notalib.django.auth.StaticBackend
#### notalib.django.auth.SettingsBackend
#### notalib.django.colorlog.ColorFormatter
#### notalib.django.filterset :fire:
#### notalib.django.formplus.MonthField
#### notalib.django.formplus.ChoiceWithDefault
#### notalib.django.formplus.IntegerArrayField
#### notalib.django.formplus.StringArrayField
#### notalib.django.formplus.MonthArrayField
#### notalib.django.request_time_middleware.RequestTimeLoggingMiddleware
