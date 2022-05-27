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
