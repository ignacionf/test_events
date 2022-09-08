from django.test import TestCase
from django.contrib.auth.models import User
from rooms.models import Room
from .models import Event


class EventTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test", email="test@test.com")
        User.objects.create(username="test2", email="test@test.com")
        User.objects.create(username="test3", email="test@test.com")
        room = Room.objects.create(name="Test Room", capacity=2)
        Event.objects.create(
            name="Test Event", room=room, private=False, date="2022-09-01"
        )

    def test_event_can_book(self):
        event = Event.objects.get(pk=1)
        user = User.objects.first()
        self.assertEqual(event.customers.count(), 0)
        event.customers.add(user)
        self.assertEqual(event.customers.count(), 1)

    def test_event_can_book_again(self):
        event = Event.objects.get(pk=1)
        user = User.objects.first()
        event.customers.add(user)
        self.assertEqual(event.customers.count(), 1)
        event.customers.add(user)
        self.assertEqual(event.customers.count(), 1)

    def test_event_can_book_exceed_capacity(self):
        event = Event.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        user3 = User.objects.get(pk=3)
        event.customers.add(user1)
        event.customers.add(user2)
        with self.assertRaises(Exception):
            event.customers.add(user3)
