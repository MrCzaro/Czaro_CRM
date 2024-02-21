from datetime import date
from django.test import TestCase

from main.models import User
from patient.models import Patient

class PatientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            date_of_birth=date(1999,9,9),
            contact_number="+48600500400",
            is_insured=True,
            insurance="1234567890",
            country="Country",
            city="City",
            street="Street",
            zip_code="00-00",
            created_by=cls.user
        )
    
    def test_valid_patient(self):
        self.assertEqual(self.patient.first_name, "Stefan")
        self.assertEqual(self.patient.last_name, "Master")
        self.assertEqual(self.patient.date_of_birth, date(1999,9,9))
        self.assertEqual(self.patient.contact_number, "+48600500400")
        self.assertEqual(self.patient.is_insured, True)
        self.assertEqual(self.patient.insurance, "1234567890")
        self.assertEqual(self.patient.country, "Country")
        self.assertEqual(self.patient.street, "Street")
        self.assertEqual(self.patient.zip_code, "00-00")
        self.assertEqual(self.patient.created_by, self.user)
        self.assertIsNotNone(self.patient.created_at)
        self.assertIsNotNone(self.patient.modified_at)
        self.assertLessEqual(self.patient.created_at, self.patient.modified_at)
        
    def test_first_name_label(self):
        field_label = self.patient._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")
        
    def test_last_name_label(self):
        field_label = self.patient._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")
        
    def test_date_of_birth_label(self):
        field_label = self.patient._meta.get_field("date_of_birth").verbose_name
        self.assertEqual(field_label, "date of birth")
        
    def test_contact_number_label(self):
        field_label = self.patient._meta.get_field("contact_number").verbose_name
        self.assertEqual(field_label, "contact number")
        
    def test_is_insured_label(self):
        field_label = self.patient._meta.get_field("is_insured").verbose_name
        self.assertEqual(field_label, "is insured")
        
    def test_insurance_label(self):
        field_label = self.patient._meta.get_field("insurance").verbose_name
        self.assertEqual(field_label, "insurance")
        
    def test_country_label(self):
        field_label = self.patient._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")
        
    def test_city_label(self):
        field_label = self.patient._meta.get_field("city").verbose_name
        self.assertEqual(field_label, "city")
        
    def test_street_label(self):
        field_label = self.patient._meta.get_field("street").verbose_name
        self.assertEqual(field_label, "street")
        
    def test_zip_code_label(self):
        field_label = self.patient._meta.get_field("zip_code").verbose_name
        self.assertEqual(field_label, "zip code")
        
    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.patient.first_name} {self.patient.last_name}"
        self.assertEqual(str(self.patient), expected_str)
    
        