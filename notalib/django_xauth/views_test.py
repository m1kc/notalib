from notalib.django_xauth.views import auth_view, logout_view
from notalib.test_fakes import FakeFunction

from unittest.mock import patch

from django.http.request import HttpRequest


def test_auth_view():
	request = HttpRequest()
	fake_authenticate = FakeFunction()
	fake_login = FakeFunction()

	with patch("notalib.django_xauth.views.authenticate", new=fake_authenticate):
		with patch("notalib.django_xauth.views.login", new=fake_login):
			response = auth_view(request)
			assert fake_login.call_count == 0
			assert fake_authenticate.call_count == 1
			assert fake_authenticate.last_call_args[0] is request
			assert fake_authenticate.last_call_kwargs == {'username': None, 'password': None}
			assert response.status_code == 403
			assert response.content == b'{"result": "fail"}'

			fake_authenticate.return_value = "USER INSTANCE"
			response = auth_view(request)

			assert fake_login.call_count == 1
			assert fake_login.last_call_args[0] is request
			assert fake_login.last_call_args[1] == "USER INSTANCE"
			assert response.status_code == 200
			assert response.content == b'{"result": "ok"}'


def test_logout_view():
	request = HttpRequest()
	fake_logout = FakeFunction()

	with patch("notalib.django_xauth.views.logout", new=fake_logout):
		response = logout_view(request)
		assert fake_logout.call_count == 1
		assert fake_logout.last_call_args[0] is request
		assert response.status_code == 200
		assert response.content == b'{"result": "ok"}'
