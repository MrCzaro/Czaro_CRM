from datetime import date
from django.test import TestCase

from scales.models import BodyMassIndex, GlasgowComaScale, NortonScale, NewsScale, PainScale
from department.models import Department, Hospitalization
from main.models import User
from patient.models import Patient

class BodyMassIndexModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.department = Department.objects.create(
                name="Test Department",
                description="This is a test department",
                created_by=cls.user
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
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )
        cls.body_mass_index = BodyMassIndex.objects.create(
            hospitalization = cls.hospitalization,
            created_by=cls.user,
            body_height=170,
            body_weight=70,
        )

    def test_valid_body_mass_index(self):
        self.assertEqual(self.body_mass_index.body_height, 170)
        self.assertEqual(self.body_mass_index.body_weight, 70)
        self.assertIsNotNone(self.body_mass_index.created_at)
        self.assertIsNotNone(self.body_mass_index.modified_at)
        self.assertEqual(self.body_mass_index.created_by, self.user)
        self.assertLessEqual(self.body_mass_index.created_at, self.body_mass_index.modified_at)
        self.assertEqual(self.body_mass_index.interpretation, "Normal weight")
        
    def test_body_height_label(self):
        field_label = self.body_mass_index._meta.get_field("body_height").verbose_name
        self.assertEqual(field_label, "body height")
        
    def test_body_weight_label(self):
        field_label = self.body_mass_index._meta.get_field("body_weight").verbose_name
        self.assertEqual(field_label, "body weight")
    
    def test_bmi_calculate(self):
        self.assertEqual(self.body_mass_index.calculate_bmi(), 24.2)
        
    def test_save_method(self):
        body_mass_index = BodyMassIndex(
            hospitalization=self.hospitalization,
            created_by = self.user,
            body_height=180,
            body_weight=80,
        )
        body_mass_index.save()
        self.assertIsNotNone(body_mass_index.bmi)
        self.assertIsNotNone(body_mass_index.interpretation)
        
        
    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.body_mass_index.hospitalization.patient.first_name} {self.body_mass_index.bmi}-points: {self.body_mass_index.interpretation}"
        self.assertEqual(str(self.body_mass_index), expected_str)
        
class GlasgowComaScaleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.department = Department.objects.create(
                name="Test Department",
                description="This is a test department",
                created_by=cls.user
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
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )
        cls.glasgow = GlasgowComaScale.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            eye_response="4",
            verbal_response="3",
            motor_response="5",
        )
        
    def test_valid_glasgow_coma_scale(self):
        self.assertEqual(self.glasgow.eye_response,"4")
        self.assertEqual(self.glasgow.verbal_response,"3")
        self.assertEqual(self.glasgow.motor_response, "5")
        self.assertEqual(self.glasgow.created_by, self.user)
        
    def test_calculate_total_points(self):
        self.assertEqual(self.glasgow.total_points, 12)
        
    def test_save_method(self):
        glasgow = GlasgowComaScale(
            hospitalization=self.hospitalization,
            created_by=self.user,
            eye_response="4",
            verbal_response="5",
            motor_response="6",
        )
        glasgow.save()
        self.assertIsNotNone(glasgow.total_points)
        
    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.glasgow.hospitalization.patient.first_name}"
        self.assertEqual(str(self.glasgow), expected_str)