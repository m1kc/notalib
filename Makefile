lint:
	poetry run flake8 --select=C,F,E101,E112,E502,E72,E73,E74,E9,W291,W6 --exclude=.cache,migrations
clean:
	find -depth -name '__pycache__' -exec rm -rfv '{}' ';'
