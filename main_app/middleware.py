from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JsonErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        response_data = {
            "error": str(exception),
            "detail": exception.__class__.__name__
        }
        return JsonResponse(response_data, status=500)