from django.test import TestCase

from department.models import Department, Hospitalization, Consultation, Observation, VitalSigns
from patient.models import Patient
from main.models import User
from datetime import date


class DepartmentModelTest(TestCase):
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
            created_by=cls.user)
        
        cls.department_uuid = cls.department.id
   
    def test_valid_hospitalization(self):
        self.assertIsNotNone(self.department.created_at)
        self.assertEqual(self.department.name, "Test Department")
        self.assertEqual(self.department.description, "This is a test department")
        self.assertEqual(self.department.created_by, self.user)
  
    def test_name_label(self):
        field_label = self.department._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")
        
    def test_description_label(self):
        field_label = self.department._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")
        
    def test_string_representation(self):
        # Test the __str__ representation
        self.assertEqual(str(self.department), "Test Department")
        
class HospitalizationModelTest(TestCase):
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

    def test_valid_hospitalization(self):
        self.assertEqual(self.hospitalization.patient, self.patient)
        self.assertEqual(self.hospitalization.department, self.department)
        self.assertIsNotNone(self.hospitalization.admitted_on)
        self.assertIsNone(self.hospitalization.dicharged_on)
        self.assertFalse(self.hospitalization.is_discharged)
        self.assertEqual(self.hospitalization.main_symptom, "Cough")
        self.assertEqual(self.hospitalization.additional_symptoms, "Fever")
 
        
    def test_main_symptom_label(self):
        field_label = self.hospitalization._meta.get_field("main_symptom").verbose_name
        self.assertEqual(field_label, "main symptom")
        
    def test_additional_symptoms_label(self):
        field_label = self.hospitalization._meta.get_field("additional_symptoms").verbose_name
        self.assertEqual(field_label, "additional symptoms")
    
    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.patient.first_name} {self.patient.last_name} - {self.department.name}"
        self.assertEqual(str(self.hospitalization), expected_str)
        
        
class ConsultationModelTest(TestCase):
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
        cls.consultation = Consultation.objects.create(
            hospitalization = cls.hospitalization,
            consultation_name = "Test Consultation",
            consultation = "This is content for a test.",
            created_by = cls.user
        )

        
    def test_valid_consultation(self):
        self.assertEqual(self.consultation.consultation_name, "Test Consultation")
        self.assertEqual(self.consultation.consultation, "This is content for a test.")
        self.assertEqual(self.consultation.hospitalization, self.hospitalization)
        self.assertIsNotNone(self.consultation.created_at)
        self.assertIsNotNone(self.consultation.modified_at)
        self.assertEqual(self.consultation.created_by, self.user)
        self.assertLessEqual(self.consultation.created_at, self.consultation.modified_at)
    
    def test_consultation_name_label(self):
        field_label = self.consultation._meta.get_field("consultation_name").verbose_name
        self.assertEqual(field_label, "consultation name")
        
    def test_consultation_label(self):
        field_label = self.consultation._meta.get_field("consultation").verbose_name
        self.assertEqual(field_label, "consultation")

        
    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.consultation.created_by} - {self.consultation.created_at}"
        self.assertEqual(str(self.consultation), expected_str)
        

        
class ObservationModelTest(TestCase):
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
        cls.hospitalization=Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )
        cls.observation=Observation.objects.create(
            hospitalization=cls.hospitalization,
            observation="Observation 1",
            created_by = cls.user,
        )

    
    def test_valid_observation(self):
        self.assertEqual(self.observation.observation, "Observation 1")
        self.assertEqual(self.observation.hospitalization, self.hospitalization)
        self.assertIsNotNone(self.observation.created_at)
        self.assertIsNotNone(self.observation.modified_at)
        self.assertEqual(self.observation.created_by, self.user)
        self.assertLessEqual(self.observation.created_at, self.observation.modified_at)
    
    def test_observation_label(self):
        field_label = self.observation._meta.get_field("observation").verbose_name
        self.assertEqual(field_label, "observation")
              
    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.observation.created_by} - {self.observation.created_at}"
        self.assertEqual(str(self.observation), expected_str)
        

class VitalSignsModelTest(TestCase):
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
        cls.vital = VitalSigns.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            systolic_blood_pressure=120,
            diastolic_blood_pressure=70,
            respiratory_rate=20,
            oxygen_saturation=100,
            temperature=37.2,
            heart_rate=88,
        )

    def test_valid_vitalsigns(self):
        self.assertEqual(self.vital.systolic_blood_pressure, 120)
        self.assertEqual(self.vital.diastolic_blood_pressure, 70)
        self.assertEqual(self.vital.respiratory_rate, 20)
        self.assertEqual(self.vital.oxygen_saturation, 100)
        self.assertEqual(self.vital.temperature, 37.2)
        self.assertEqual(self.vital.heart_rate, 88)
        self.assertEqual(self.vital.hospitalization, self.hospitalization)
        self.assertIsNotNone(self.vital.created_at)
        self.assertIsNotNone(self.vital.modified_at)
        self.assertEqual(self.vital.created_by, self.user)
        self.assertLessEqual(self.vital.created_at, self.vital.modified_at)
        
    def test_systolic_blood_pressure_label(self):
        field_label = self.vital._meta.get_field("systolic_blood_pressure").verbose_name
        self.assertEqual(field_label, "systolic blood pressure")
        
    def test_systolic_diastolic_blood_pressure_label(self):
        field_label = self.vital._meta.get_field("diastolic_blood_pressure").verbose_name
        self.assertEqual(field_label, "diastolic blood pressure")
    
    def test_respiratory_rate_label(self):
        field_label = self.vital._meta.get_field("respiratory_rate").verbose_name
        self.assertEqual(field_label, "respiratory rate")
    
    def test_oxygen_saturation_label(self):
        field_label = self.vital._meta.get_field("oxygen_saturation").verbose_name
        self.assertEqual(field_label, "oxygen saturation")
    
    def test_temperature_label(self):
        field_label = self.vital._meta.get_field("temperature").verbose_name
        self.assertEqual(field_label, "temperature")
        
    def test_heart_rate_label(self):
        field_label = self.vital._meta.get_field("heart_rate").verbose_name
        self.assertEqual(field_label, "heart rate")
    
    
    def test_string_representation(self):
        expected_str = f"{self.vital.created_by} - {self.vital.created_at}"
        self.assertEqual(str(self.vital), expected_str)
        
    

