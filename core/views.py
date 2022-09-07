from django.http import JsonResponse


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': str(exception) if exception else "Not Found"
    })
