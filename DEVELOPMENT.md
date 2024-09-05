# Development howtos

## Install git version

```
poetry add 'git+https://github.com/m1kc/notalib.git@master'
```

## Prepare a release

1. Bump package version in `pyproject.toml` on `master`, commit message: `v1.1.1`
2. `poetry build`
3. `poetry publish`
4. Create and push tag
5. Publish release notes

## Login to PyPI with Poetry

> Source: https://python-poetry.org/docs/repositories/

To publish to PyPI, you can set your credentials for the repository named `pypi`.

Note that it is recommended to use API tokens when uploading packages to PyPI. Once you have created a new token, you can tell Poetry to use it:

```
poetry config pypi-token.pypi <token>
```

If you still want to use your username and password, you can do so with the following call to config.

```
poetry config http-basic.pypi <username> <password>
```

If you want to use plaintext config instead of keyring:

```
poetry config keyring.enabled false
```
