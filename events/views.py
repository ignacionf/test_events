import json

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from .models import Event
from .forms import EventForm


class EventView(View, LoginRequiredMixin):
    form_class = EventForm

    @method_decorator(login_required)
    @method_decorator(permission_required("events.view_event"))
    def get(self, request, pk=None):
        queryset = Event.objects.filter(private=False)

        if pk:
            instance = get_object_or_404(queryset, pk=pk)
            booked_count = instance.customers.count()
            data = {
                "id": instance.id,
                "name": instance.name,
                "date": instance.date,
                "capacity": {
                    "max": instance.room.capacity,
                    "booked": booked_count,
                    "available": instance.room.capacity - booked_count,
                },
            }
            return JsonResponse(data)

        return JsonResponse({"events": list(queryset.values())})

    @method_decorator(login_required)
    @method_decorator(permission_required("events.add_event"))
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
    @method_decorator(permission_required("events.delete_event"))
    def delete(self, request, pk):
        get_object_or_404(Event, pk=pk).delete()
        return JsonResponse({"status": "sucess"})


class BookView(View, LoginRequiredMixin):
    @method_decorator(login_required)
    @method_decorator(permission_required("events.view_event"))
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk, private=False)

        if event.customers.filter(id=request.user.id):
            return JsonResponse({"status": "you are registered for this event"})

        return JsonResponse({"status": "you aren't registered for this event"})

    @method_decorator(login_required)
    @method_decorator(permission_required("events.change_event"))
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk, private=False)

        if event.customers.filter(id=request.user.id):
            return JsonResponse({"status": "already booked"}, status=304)

        try:
            event.customers.add(request.user)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)

        return JsonResponse({"status": "booked"})

    @method_decorator(login_required)
    @method_decorator(permission_required("events.change_event"))
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk, private=False)

        if not event.customers.filter(id=request.user.id):
            return JsonResponse({"status": "not booked"}, status=304)

        event.customers.remove(request.user)

        return JsonResponse({"status": "unbooked :P"})
