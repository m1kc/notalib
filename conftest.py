from django.conf import settings

def pytest_configure():
	settings.configure(
		USE_I18N=False,
	)
