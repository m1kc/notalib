# notalib [![Django CI](https://github.com/m1kc/notalib/actions/workflows/django.yml/badge.svg)](https://github.com/m1kc/notalib/actions/workflows/django.yml) [![Coverage Status](https://coveralls.io/repos/github/m1kc/notalib/badge.svg?branch=master)](https://coveralls.io/github/m1kc/notalib?branch=master)

Collection of small Python utility functions and classes. Some are written by me, some are taken from StackOverflow and customized (I tried to provide links to original sources where possible). This repo never aimed to be a library of any sort (but now it is).

## Install

```sh
pip install notalib
```

Or with [poetry](https://python-poetry.org/):

```sh
poetry add notalib
```

## Maintenance & bugfixes

While I try to fix bugs, add new features, and review any PRs when I have time, there're no promises and no set timeframes, even if a bug is critical. That's a project I do in my free time, free of charge.

If that's not enough for you or you have an urgent request, there are paid maintenance options (bugfixing, features, expedite PR review, 24h security responses). Contact me for prices: m1kc@yandex.ru

Also feel free to just send me money:

* MasterCard: 5559 4925 7484 0297
* PayPal: [paypal.me/thisism1kc](https://paypal.me/thisism1kc)

Donations are always appreciated, even if you send 10$.

## Constants included

* `notalib.utf.BOM`: contains string `b'\xEF\xBB\xBF'` (UTF-8 little endian byte order mark).

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
#### notalib.date.get_week_number

Returns week number for the given Arrow date.

```python
get_week_number(arrow.get('2021-12-31'))
# 53
get_week_number(arrow.get('2022-01-01'))
# 1
get_week_number(arrow.get('2022-01-06'))
# 2
```

#### notalib.dict.find_field
#### notalib.dict.find_value
#### notalib.dict.normalize_dict :fire:
#### notalib.dict.filter_dict

Filters a dictionary, removing any keys except for the ones you choose.

```python
src = {
	'Some': "BODY",
	'once': "told me",
	'the world': "is gonna roll me",
}
filtered_dict(src, ["Some", "once"])
# {'Some': 'BODY', 'once': 'told me'}
filtered_dict(src, [])
# {}
```

#### notalib.format.format_long_list
#### notalib.hypertext.strip_tags :fire:
#### notalib.hypertext.TablePrinter :fire:

Prints an HTML table, row by row, from the given data, using attrs or dictionary keys as columns.

Two ways to use it:

* Call header() / entry() / footer() manually

```python
from notalib.hypertext import TablePrinter
t = TablePrinter(['a', 'b'])
t.header()
# '<table><thead><tr><th>a</th><th>b</th></tr></thead><tbody>'
t.entry({'a': 1, 'b': 2})
# '<tr><td>1</td><td>2</td></tr>\n'
t.entry({'a': 11, 'b': 22})
# '<tr><td>11</td><td>22</td></tr>\n'
t.footer()
# '</tbody></table>'
```

* Pass an iterable to iterator_over()
	
```python
from notalib.hypertext import TablePrinter
t = TablePrinter(['a', 'b'])
list(t.iterator_over([ {'a': 11, 'b': 22} ]))
# ['<table><thead><tr><th>a</th><th>b</th></tr></thead><tbody>',
#  '<tr><td>11</td><td>22</td></tr>\n',
#  '</tbody></table>']
```

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
#### notalib.pandas.pandasplus.replace_null_objects

Replaces all types of null values in a DataFrame with the given value.

```python
df = pd.DataFrame({'A': [pd.NA, pd.NaT, 'SomeVal', None]})
new_df = replace_null_objects(df, "Hello, notalib!")
new_df
#                  A
# 0  Hello, notalib!
# 1  Hello, notalib!
# 2          SomeVal
# 3  Hello, notalib!
```

## Django-related

#### notalib.django.auth.StaticBackend
#### notalib.django.auth.SettingsBackend

#### notalib.django.xauth

Endpoints for easier authentication in APIs. Requires Django REST framework.

Provides endpoints:

* `/xauth/check` — returns code 200 if client is authenticated (or global permissions are set to AllowAny), 403 if not
* `/xauth/auth-post` — authenticates a client; accepts two POST parameters `username` and `password`; returns code 200 on success and 403 on failure

How to use:

1. Make sure Django REST framework is installed.
2. Add `'notalib.django_xauth'` to INSTALLED_APPS.
3. Run `manage.py migrate django_xauth` (doesn't actually change your DB).
4. Add something like this to your urls.py: `path('xauth/', include('notalib.django_xauth.urls')),`

#### notalib.django.colorlog.ColorFormatter
#### notalib.django.filterset :fire:
#### notalib.django.formplus.MonthField
#### notalib.django.formplus.ChoiceWithDefault
#### notalib.django.formplus.IntegerArrayField
#### notalib.django.formplus.StringArrayField
#### notalib.django.formplus.MonthArrayField
#### notalib.django.request_time_middleware.RequestTimeLoggingMiddleware
#### notalib.django.stream.stream_json

Stream all elements of iterable object as JSON array using the StreamingHttpResponse class. Unlike DRF's Response class, it can handle arrays of any size.

```python
class SomeViewSet(...):
    ...
    
    def list(self, request, *args, **kwargs):
        ...
        return stream_json(data)
```

## Django/Clickhouse

_Stage: alpha_

Required packages: `clickhouse-sqlalchemy`

Required two django.settings variables:

* **CLICKHOUSE_URL** — database URL
* **CLICKHOUSE_PROFILE** — dump all queries and their timing to console, true/false

#### notalib.django.clickhouse.base.get_connection
#### notalib.django.clickhouse.base.get_database_name
#### notalib.django.clickhouse.base.Query

A wrapper for SQLAlchemy's `select` with some useful postprocessing options.

* `execute` — no postprocessing
* `execute_val` — returns single value
* `execute_list` — returns single column as list
* `execute_kv` — returns dict, first column becomes keys, second column becomes values
* `execute_na` — returns number of affected rows

Usage example:

```python
q = Query(
    select([ SomeTable.c.notalib ])
)
q.execute_list()
# ["Example", "OOOOO", "my", "defence", ...]
```

#### notalib.django.clickhouse.mutations.get_mutations_in_progress_count

Returns the number of mutations in progress for the specified table.

```python
get_mutations_in_progress_count("SOME_DATABASE", "SOME_TABLE_IN_DATABASE")
# 5
```

#### notalib.django.clickhouse.wait.wait_result :fire:

Waits until all mutations for the given table are complete.

```python
# blah blah blah, ALTER TABLE ... UPDATE ...
wait_result("SOME_DATABASE", "SOME_TABLE_IN_DATABASE")
# UPDATE complete, continue
```
