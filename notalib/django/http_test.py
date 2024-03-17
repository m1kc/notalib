from notalib.django.http import HttpResponseSeeOther, HttpResponseTemporaryRedirect

from http import HTTPStatus


class TestHttpResponseSeeOther:
	def test_cls_attrs(self):
		assert HttpResponseSeeOther.status_code == HTTPStatus.SEE_OTHER.value


class TestHttpResponseTemporaryRedirect:
	def test_cls_attrs(self):
		assert HttpResponseTemporaryRedirect.status_code == HTTPStatus.TEMPORARY_REDIRECT.value
