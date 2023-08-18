from django.http import HttpResponseRedirect


class HttpResponseSeeOther(HttpResponseRedirect):
	status_code = 303


class HttpResponseTemporaryRedirect(HttpResponseRedirect):
	status_code = 307
