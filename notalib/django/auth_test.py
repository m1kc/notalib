from notalib.django.auth import StaticBackend, SettingsBackend
from notalib.test_fakes import FakeFunction

from unittest.mock import patch

from django.http.request import HttpRequest
from django.contrib.auth.models import User


class FakeUserGetter(FakeFunction):
	def __init__(self, return_value, with_error = False):
		super().__init__(return_value)
		self.with_error = with_error

	def __call__(self, *args, **kwargs) -> User:
		self.last_call_args = args
		self.last_call_kwargs = kwargs
		self.call_count += 1

		if self.with_error:
			raise User.DoesNotExist()

		return self.return_value


class TestStaticBackend:
	def test_authenticate(self, settings):
		settings.STATIC_AUTH_CREDENTIALS = {}

		backend = StaticBackend()
		assert backend.authenticate(HttpRequest(), "john", "doe") is None

		settings.STATIC_AUTH_CREDENTIALS = {"john": "lennon"}
		assert backend.authenticate(HttpRequest(), "john", "doe") is None

		with patch.object(backend, "_get_or_create", return_value=123):
			assert backend.authenticate(HttpRequest(), "john", "lennon") == 123

	def test__get_or_create(self):
		backend = StaticBackend()
		user = User(username="john")
		user_getter = FakeUserGetter(user, False)

		with patch("notalib.django.auth.User.objects.get", new=user_getter):
			assert backend._get_or_create("john") is user
			assert user_getter.call_count == 1
			assert user_getter.last_call_args == ()
			assert user_getter.last_call_kwargs == {"username": "john"}

			user_getter.with_error = True
			user_getter.return_value = None
			with patch("notalib.django.auth.User.save", new=FakeFunction()):
				new_user = backend._get_or_create("john-doe")
				assert isinstance(new_user, User)
				assert new_user.username == "john-doe"
				assert user_getter.call_count == 2
				assert user_getter.last_call_args == ()
				assert user_getter.last_call_kwargs == {"username": "john-doe"}

	def test_get_user(self):
		backend = StaticBackend()
		user = User(pk=1)
		user_getter = FakeUserGetter(user, False)

		with patch("notalib.django.auth.User.objects.get", new=user_getter):
			assert backend.get_user(1) is user
			assert user_getter.call_count == 1
			assert user_getter.last_call_args == ()
			assert user_getter.last_call_kwargs == {"pk": 1}

			user_getter.with_error = True
			user_getter.return_value = None
			with patch("notalib.django.auth.User.save", new=FakeFunction()):
				assert backend.get_user(1) is None


class TestSettingsBackend:
	def test_authenticate(self, settings):
		settings.ADMIN_LOGIN = "username_admin"
		settings.ADMIN_PASSWORD = "password_admin"

		backend = SettingsBackend()
		user = User(username="username_admin")
		fake_password_check = FakeFunction(False)
		fake_user_getter = FakeUserGetter(user)
		fake_user_saver = FakeFunction()

		with patch("notalib.django.auth.check_password", new=fake_password_check):
			assert backend.authenticate(HttpRequest(), "username_user", "password_user") is None
			assert fake_password_check.call_count == 1
			assert fake_password_check.last_call_args == ("password_user", "password_admin")

			fake_password_check.return_value = True

			with patch("notalib.django.auth.User.objects.get", new=fake_user_getter):
				assert backend.authenticate(HttpRequest(), "username_admin", "password_admin") is user
				assert fake_password_check.call_count == 2
				assert fake_password_check.last_call_args == ("password_admin", "password_admin")
				assert fake_user_getter.call_count == 1
				assert fake_user_getter.last_call_kwargs == {"username": "username_admin"}

				fake_user_getter.with_error = True

				with patch("notalib.django.auth.User.save", new=fake_user_saver):
					user = backend.authenticate(HttpRequest(), "username_admin", "password_admin")
					assert user.username == "username_admin"
					assert user.is_staff and user.is_superuser
					assert fake_user_saver.call_count == 1
					assert fake_user_getter.call_count == 2
					assert fake_user_getter.last_call_kwargs == {"username": "username_admin"}
					assert fake_password_check.call_count == 3
					assert fake_password_check.last_call_args == ("password_admin", "password_admin")

	def test_get_user(self):
		backend = SettingsBackend()
		user = User(pk=1)
		user_getter = FakeUserGetter(user, False)

		with patch("notalib.django.auth.User.objects.get", new=user_getter):
			assert backend.get_user(1) is user
			assert user_getter.call_count == 1
			assert user_getter.last_call_args == ()
			assert user_getter.last_call_kwargs == {"pk": 1}

			user_getter.with_error = True
			user_getter.return_value = None
			with patch("notalib.django.auth.User.save", new=FakeFunction()):
				assert backend.get_user(1) is None
