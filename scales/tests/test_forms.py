from django.test import TestCase
from main.models import User
from scales.forms import BodyMassIndexForm

class BodyMassIndexForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )