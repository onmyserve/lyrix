from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Customer


class CoreModelsTest(TestCase):
    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com"
        )
        self.assertEqual(str(profile), "Jane Doe")

    def test_create_customer(self):
        customer = Customer.objects.create(
            first_name="John",
            last_name="Smith",
            email="john@example.com"
        )
        self.assertEqual(str(customer), "John Smith")
