from social_django.middleware import SocialAuthExceptionMiddleware
from django.shortcuts import HttpResponse
from social_django.middleware import exceptions as social_exceptions

class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
	def process_exception(self, request, exception):
		if hasattr(social_exceptions, 'AuthCanceled'):
			return HttpResponse('/')
		else:
			raise exception