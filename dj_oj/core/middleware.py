from django.shortcuts import render
from django_ratelimit.exceptions import Ratelimited


class RateLimitExceptionMiddleware:
    template_name = 'core/errors/ratelimit.html'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, Ratelimited):
            return
        
        ctx = getattr(request.user, '_ratelimit_exception_context', {})
        return render(request, self.template_name, ctx)
