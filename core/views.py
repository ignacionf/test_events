from django.http import JsonResponse


def custom404(request, exception=None):

    msg = "Not found"
    # just get the message if i raise this exception
    if isinstance(exception.args[0], str):
        msg = str(exception.args[0])
    return JsonResponse({"status_code": 404, "error": msg})
