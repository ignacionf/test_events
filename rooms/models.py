from django.db import models


class Room(models.Model):
    name = models.CharField("Name", max_length=100)
    capacity = models.PositiveSmallIntegerField("Max Capacity")

    def __str__(self):
        return f"{self.name}:{self.capacity}"
