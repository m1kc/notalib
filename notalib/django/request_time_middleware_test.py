from notalib.django.request_time_middleware import RequestTimeLoggingMiddleware
from notalib.test_fakes import FakeFunction

from http import HTTPStatus
from datetime import datetime, timezone
from unittest.mock import patch

from django.http.request import HttpRequest
from django.http.response import HttpResponse


class TestRequestTimeLoggingMiddleware:
	def test_log_message(self, capsys):
		dt = datetime(2024, 1, 1, 12, 30, 30, 500, tzinfo=timezone.utc)

		with patch("notalib.django.request_time_middleware.datetime.datetime") as dt_mock:
			dt_mock.utcnow.return_value = dt

			with patch("notalib.django.request_time_middleware.uuid") as uuid_mock:
				uuid = "uuid1:00000000000000000000"
				uuid_mock.uuid1.return_value = uuid
				request = HttpRequest()
				request.path = "/dev/null"
				RequestTimeLoggingMiddleware.log_message(request, "TAG", "MESSAGE")
				captured = capsys.readouterr()
				assert captured.out == f"2024-01-01T12:30:30.000500+00:00 TAG        {uuid}  1 /dev/null +0:00:00 MESSAGE\n"


	def test_process_request(self):
		middleware = RequestTimeLoggingMiddleware()
		request = HttpRequest()
		fake_log_message = FakeFunction()

		with patch.object(middleware, "log_message", new=fake_log_message):
			middleware.process_request(request)

		assert fake_log_message.call_count == 1
		assert fake_log_message.last_call_args == (request, 'request ')

	def test_process_response(self):
		middleware = RequestTimeLoggingMiddleware()
		request = HttpRequest()
		response = HttpResponse()
		fake_log_message = FakeFunction()

		with patch.object(middleware, "log_message", new=fake_log_message):
			assert middleware.process_response(request, response) is response
			assert fake_log_message.call_count == 1
			assert fake_log_message.last_call_args == (request, "response", "200")

			for status_code in (
				HTTPStatus.MULTIPLE_CHOICES.value,
				HTTPStatus.MOVED_PERMANENTLY.value,
				HTTPStatus.FOUND.value,
				HTTPStatus.TEMPORARY_REDIRECT.value,
			):
				response.status_code = status_code
				assert middleware.process_response(request, response) is response
				assert fake_log_message.last_call_args == (request, "response", f"{status_code} => ?")

			response['Location'] = "unknown"
			assert middleware.process_response(request, response) is response
			assert fake_log_message.call_count == 6
			assert fake_log_message.last_call_args == (request, "response", f"{status_code} => unknown")

			response.status_code = 200
			response.content = b'deadbee'
			assert middleware.process_response(request, response) is response
			assert fake_log_message.call_count == 7
			assert fake_log_message.last_call_args == (request, "response", "200 (7b)")
