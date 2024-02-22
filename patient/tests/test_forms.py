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
        
    def test_form_initialization(self):
        form = PatientForm()
        self.assertIsInstance(form, PatientForm)
        
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
        
        self.assertTrue(form.is_valid())
     
    def test_invalid_form(self):
        # Empty form
        data = {}
        form = PatientForm(data)
        self.assertFalse(form.is_valid())
        
        # Missing fields
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
        self.assertTrue(form.is_valid())
        
        patient = form.save(commit=False)
        patient.created_by = self.user
        patient.save()
        
        self.assertIsInstance(patient, Patient)
    
    def test_first_name_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["first_name"].label, "First Name:")
        
    def test_last_name_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["last_name"].label, "Last Name:")
        
    def test_date_of_birth_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["date_of_birth"].label, "Date of Birth:")
        
    def test_contact_number_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["contact_number"].label, "Telephone number:")
        
    def test_is_insured_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["is_insured"].label, "Insured:")
        
    def test_insurance_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["insurance"].label, "Insurance Number:")
        
    def test_country_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["country"].label, "Country:")
        
    def test_city_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["city"].label, "City:")
            
    def test_street_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["street"].label, "Street adress:")
            
    def test_zip_code_label(self):
        form = PatientForm()
        self.assertEqual(form.fields["zip_code"].label, "Zip-code:")
    

