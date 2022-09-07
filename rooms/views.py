import json

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from .models import Room
from .forms import RoomForm


class RoomView(View, LoginRequiredMixin):
    form_class = RoomForm

    @method_decorator(login_required)
    @method_decorator(permission_required("rooms.view_room"))
    def get(self, request, pk=None):
        queryset = Room.objects.all()

        if pk:
            instance = get_object_or_404(queryset, pk=pk)
            return JsonResponse(model_to_dict(instance))

        return JsonResponse({"rooms": list(queryset.values())})

    @method_decorator(login_required)
    @method_decorator(permission_required("rooms.add_room"))
    def post(self, request, *args, **kwargs):

        if request.POST:
            data = request.POST
        else:
            data = json.loads(request.body)

        form = self.form_class(data)

        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance))

        return JsonResponse({"errors": form.errors.as_json()})

    @method_decorator(login_required)
    @method_decorator(permission_required("rooms.delete_room"))
    def delete(self, request, pk):
        get_object_or_404(Room, pk=pk).delete()
        return JsonResponse({"status": "sucess"})
