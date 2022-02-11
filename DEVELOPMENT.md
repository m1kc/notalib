# Development howtos

## Install git version

```
poetry add 'git+https://github.com/m1kc/notalib.git@master'
```

## Prepare a release

1. Bump package version in `pyproject.toml` on `master`
2. `poetry build`
3. `poetry publish`
4. Merge branch `master` into `stable`
5. Create and push tag
6. Publish release notes
