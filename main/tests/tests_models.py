from django.test import TestCase
from main.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(
            first_name="Nurse",
            last_name="User",
            email="testnurse@admin.com",
            password="nursepassword",
            profession="nurses",
        )
        cls.admin = User.objects.create_superuser(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
    def test_valid_normaluser(self):
        self.assertEqual(self.user.first_name, "Nurse")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.email, "testnurse@admin.com")
        self.assertEqual(self.user.profession, "nurses")
        self.assertTrue(self.user.check_password("nursepassword"))
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(str(self.user), "testnurse@admin.com")
        self.assertIsNotNone(self.user.date_joined)
        
    
    def test_valid_superuser(self):
        self.assertEqual(self.admin.first_name, "AdminTest")
        self.assertEqual(self.admin.last_name, "User")
        self.assertEqual(self.admin.email, "testadmin@admin.com")
        self.assertEqual(self.admin.profession, "admins")
        self.assertTrue(self.admin.check_password("adminpassword"))
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
        self.assertEqual(str(self.admin), "testadmin@admin.com")
        self.assertIsNotNone(self.admin.date_joined)
        