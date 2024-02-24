import uuid

from django.test import TestCase, Client
from django.urls import reverse
from main.models import User
from department.models import Department, Hospitalization
from patient.models import Patient
from patient.forms import PatientForm

class IndexViewTest(TestCase):    
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        
    def test_authentication_required(self):
        response = self.client.get(reverse("patient:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/patient/")
    

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_list.html")
    
    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("patients", response.context)
        self.assertIn("title", response.context)
    
class PatientDetailViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.patient = Patient.objects.create(
            first_name="Stefan",
            last_name="Master",
            date_of_birth="1999-09-09",
            contact_number="+48600500400",
            is_insured=True,
            insurance="1234567890",
            country="Country",
            city="City",
            street="Street",
            zip_code="00-00",
            created_by=cls.user
        )
        
    
    def test_authentication_required(self):
        response = self.client.get(reverse("patient:detail", args=[self.patient.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/patient/{self.patient.id}/detail/")
    
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:detail", args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_detail.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:detail", args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("patient", response.context)
        self.assertIn("hospitalizations", response.context)
        self.assertIn("ongoing_admission", response.context)
        self.assertIn("title", response.context)
        self.assertIn("back_url", response.context)
        
    def test_404_response_invalid_patient_id(self):
        invalid_id = uuid.uuid4() 
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:detail", args=[invalid_id]))
        self.assertEqual(response.status_code, 404)
        
    def test_back_url(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:detail", args=[self.patient.id]))
        back_url = response.context["back_url"]
        self.assertEqual(back_url, reverse("patient:index"))
        
class PatientCreateViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
    
    def test_authentication_required(self):
        response = self.client.get(reverse("patient:create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/patient/add/")
    
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_form_add.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:create"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        
    def test_form_submission_valid_data(self):
        data = {
            "first_name" : "Juzef",
            "last_name" : "Patient",
            "date_of_birth" : "1992-02-02",
            "contact_number" : "+48600000000",
            "is_insured" : True,
            "insurance" : "0987654321",
            "country" : "Country",
            "city" : "City",
            "street" : "Street",
            "zip_code" : "00-00",
            "created_by": self.user    
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("patient:create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("patient:index"))
        self.assertTrue(Patient.objects.filter(first_name="Juzef", last_name="Patient").exists())
        
    def test_form_submission_invalid_data(self):
        data = {
            "first_name" : "Juzef",
            #"last_name" : "Patient",
            "date_of_birth" : "1992-02-02",
            "contact_number" : "+48600000000",
            "is_insured" : True,
            "insurance" : 0,
            "country" : "Country",
            "city" : "City",
            "street" : "Street",
            "zip_code" : "00-00",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("patient:create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_form_add.html")
        self.assertIsInstance(response.context["form"], PatientForm)
        
class PatientUpdateViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.patient = Patient.objects.create(
            first_name="Stefan",
            last_name="Master",
            date_of_birth="1999-09-09",
            contact_number="+48600500400",
            is_insured=True,
            insurance="1234567890",
            country="Country",
            city="City",
            street="Street",
            zip_code="00-00",
            created_by=cls.user
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:update", args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_form_update.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:update", args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
    
    def test_form_submission(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        data = {
            "first_name" : "Juzef",
            "last_name" : "Patient",
            "date_of_birth" : "1992-02-02",
            "contact_number" : "+48600000000",
            "is_insured" : True,
            "insurance" : "0987654321",
            "country" : "Country",
            "city" : "City",
            "street" : "Street",
            "zip_code" : "00-00",   
        }
        response = self.client.post(reverse("patient:update", args=[self.patient.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("patient:index"))
        updated_patient = Patient.objects.get(id=self.patient.id)
        self.assertEqual(updated_patient.first_name, "Juzef")

class PatientDeleteViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.patient = Patient.objects.create(
            first_name="Stefan",
            last_name="Master",
            date_of_birth="1999-09-09",
            contact_number="+48600500400",
            is_insured=True,
            insurance="1234567890",
            country="Country",
            city="City",
            street="Street",
            zip_code="00-00",
            created_by=cls.user
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:delete", args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_confirm_delete.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("patient:delete", args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context)
        self.assertIsInstance(response.context["object"], Patient)
        
    def test_patient_deletion(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("patient:delete", args=[self.patient.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("patient:index"))
        with self.assertRaises(Patient.DoesNotExist):
            deleted_patient = Patient.objects.get(id=self.patient.id)
            
