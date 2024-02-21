from django.test import TestCase
from main.models import User
from patient.forms import PatientForm
from patient.models import Patient

class PatientFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
    
    def test_valid_form(self):
        data = {
            "first_name" : "Patient",
            "last_name" : "Mr Sick",
            "date_of_birth" : "1999-09-09",
            "contact_number" : "+48600500400",
            "is_insured" : True,
            "insurance" : "1234567890",
            "country" : "Country",
            "city" : "City",
            "street" : "Street",
            "zip_code" : "00-00"
        }
        form = PatientForm(data)
        self.assertTrue(form.is_valid)
        
    def test_invalid_form(self):
        data = {
            "first_name" : "Patient",
            "last_name" : "Mr Sick",
            "date_of_birth" : "1999-09-09",
            "contact_number" : "+48600500400",
            "is_insured" : True,
            "insurance" : "1234567890",
            #"country" : "Country",
            #"city" : "City",
            #"street" : "Street",
            #"zip_code" : "00-00"
        }
        form = PatientForm(data)
        self.assertFalse(form.is_valid())
    
    def test_save_method(self):
        data = {
            "first_name" : "Patient",
            "last_name" : "Mr Sick",
            "date_of_birth" : "1999-09-09",
            "contact_number" : "+48600500400",
            "is_insured" : True,
            "insurance" : "1234567890",
            "country" : "Country",
            "city" : "City",
            "street" : "Street",
            "zip_code" : "00-00"
        }
        form = PatientForm(data)
        self.assertTrue(form.is_valid)
        
        patient = form.save(commit=False)
        patient.created_by = self.user
        patient.save()
        
        self.assertIsInstance(patient, Patient)
        
    def test_form_labels(self):
        form = PatientForm()
        self.assertTrue(form.fields["first_name"].label == "First Name:")
        self.assertTrue(form.fields["last_name"].label == "Last Name:")
        self.assertTrue(form.fields["date_of_birth"].label == "Date of Birth:")
        self.assertTrue(form.fields["contact_number"].label == "Telephone number:")
        self.assertTrue(form.fields["is_insured"].label == "Insured:")
        self.assertTrue(form.fields["insurance"].label == "Insurance Number:")
        self.assertTrue(form.fields["country"].label == "Country:")
        self.assertTrue(form.fields["city"].label == "City:")
        self.assertTrue(form.fields["street"].label == "Street adress:")
        self.assertTrue(form.fields["zip_code"].label == "Zip-code:")
        