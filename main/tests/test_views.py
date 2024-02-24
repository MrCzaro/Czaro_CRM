from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from main.models import User


class LoginViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        
        cls.client = Client()
        
    def test_successful_rendering(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertIn("title", response.context)
    
    def test_successful_login(self):
        response = self.client.post("/login/", {"email": "testadmin@admin.com", "password": "adminpassword"})
        self.assertRedirects(response, reverse("patient:index"))
        
    def test_unsuccessful_login(self):
        response = self.client.post("/login/", {"email": "wrong@email.com", "password": "wrongpassword"})
        self.assertContains(response, "Invalid login credentials. Please try again.")

class SignUpViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        
        cls.client = Client()
    def test_successful_rendering(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertIn("title", response.context)
        self.assertIn("USER_CHOICES", response.context)
    
    def test_successful_account_creation(self):
        data = {
            "first_name" : "Nurse",
            "last_name" : "Test",
            "email" : "nursetest@admin.com",
            "password1" : "123testnurse123",
            "password2" : "123testnurse123",
            "profession" : "nurses"
        }   
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:login"))
        # Check if a user was created:
        self.assertTrue(User.objects.filter(email=data["email"]).exists())
        # Check for success messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your account has been created. You can login.")
    
    def test_missing_fields(self):
        data = {
            "first_name" : "",
            "last_name" : "Test",
            "email" : "nursetest@admin.com",
            "password1" : "123testnurse123",
            "password2" : "123testnurse123",
            "profession" : "nurses"
        }  
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, 200)
        
        # Check if a user was not created
        self.assertFalse(User.objects.filter(email=data["email"]).exists())
        # Check for error messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Error while creating an account. Please provide a valid email address, name, and password.")
        
    def test_password_mismatch(self):
        data = {
            "first_name" : "Nurse",
            "last_name" : "Test",
            "email" : "nursetest@admin.com",
            "password1" : "123testnurse123",
            "password2" : "321testnurse321",
            "profession" : "nurses"
        }
        
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, 200)
        # Check if a user was not created
        self.assertFalse(User.objects.filter(email=data["email"]).exists())
        # Check for error messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your password do not match.")
    
    def test_incorrect_email(self):
        data = {
            "first_name" : "Nurse",
            "last_name" : "Test",
            "email" : "email",
            "password1" : "123testnurse123",
            "password2" : "123testnurse123",
            "profession" : "nurses"
        }
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, 200)
       
        # Check if a user was not created
        self.assertFalse(User.objects.filter(email=data["email"]).exists())
        print
        # Check for error messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please provide a valid email address.")
        
    def test_existing_email(self):
        data = {
            "first_name" : "AdminTest",
            "last_name" : "User",
            "email" : "testadmin@admin.com",
            "password1" : "adminpassword",
            "password2" : "adminpassword",
            "profession" : "admins",
        }
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, 200)
        # Check for error messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "An account with this email already exists.")