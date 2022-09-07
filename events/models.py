from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rooms.models import Room


class Event(models.Model):
    name = models.CharField("Event Name", max_length=100)
    date = models.DateField("Event date")
    private = models.BooleanField(default=False)

    customers = models.ManyToManyField(User)

    room = models.ForeignKey(Room, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = [["date", "room"]]

@receiver(m2m_changed, sender=Event.customers.through)
def event_customers_changed(sender, **kwargs):
    if kwargs.get('action') == "pre_add":
        instance = kwargs.get("instance")
        if instance.customers.count() >= instance.room.capacity:
            raise Exception("Exceeds room capacity")


