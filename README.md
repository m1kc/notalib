# notalib

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
#### notalib.array.ensure_iterable :fire:
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

The CLI progress indicator you've always dreamt of: shows current and total if available, measures current speed, can show your comments for each element, makes sure not to slow down your terminal with frequent updates. [See this short demo](https://asciinema.org/a/UI1aOqjQC1KXx303kaVGrxjQp)

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
