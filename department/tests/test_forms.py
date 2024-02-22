from django.test import TestCase

from department.models import Department, Hospitalization, Consultation, Observation, VitalSigns
from department.forms import DepartmentForm, ConsultationForm, ObservationForm, HospitalizationForm, TransferPatientForm, DischargeForm, VitalSignsForm
from patient.models import Patient
from main.models import User

class DepartmentFormTest(TestCase):
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
        form = DepartmentForm()
        self.assertIsInstance(form, DepartmentForm)
        
    def test_valid_form(self):
        data = {
            "name" : "Test Department",
            "description" : "Test Description Department",
        }
        
        form = DepartmentForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            #"name" : "Test Department",
            "description" : "Test Description Department",
        }
        form = DepartmentForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "name" : "Test Department",
            "description" : "Test Description Department",
        }
        form = DepartmentForm(data)
        self.assertTrue(form.is_valid())
        
        department = form.save(commit=False)
        department.created_by = self.user
        department.save()     
        self.assertIsInstance(department, Department)
        
class ConsulationFormTest(TestCase):
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
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
    )
        
    def test_valid_form(self):
        data = {
            "consultation_name": "Test Name of Consultation",
            "consultation": "Test Consulation",
        }
        
        form = ConsultationForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            #"consultation_name": "Test Name of Consultation",
            "consultation": "Test Consulation",
        }
        form = ConsultationForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "consultation_name": "Test Name of Consultation",
            "consultation": "Test Consulation",
        }
        form = ConsultationForm(data)
        self.assertTrue(form.is_valid())
        
        consultation = form.save(commit=False)
        consultation.created_by = self.user
        consultation.hospitalization = self.hospitalization
        consultation.save()     
        self.assertIsInstance(consultation, Consultation)

class ObservationFormTest(TestCase):
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
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
    )
        
    def test_valid_form(self):
        data = {
            "observation": "Test Observation",
        }
        
        form = ObservationForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            #"observation": "Test Observation",
        }
        form = ObservationForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "observation": "Test Observation",
        }
        form = ObservationForm(data)
        self.assertTrue(form.is_valid())
        
        observation = form.save(commit=False)
        observation.created_by = self.user
        observation.hospitalization = self.hospitalization
        observation.save()     
        self.assertIsInstance(observation, Observation)
        
class HospitalizatonFormTest(TestCase):
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
        
    def test_valid_form(self):
        data = {
            "main_symptom": "Fever",
            "additional_symptoms" : "Fatigue",
            "department_id" : self.department.id,
        }
        
        form = HospitalizationForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            #"main_symptom": "Fever",
            "additional_symptoms" : "Fatigue",
            "department_id" : self.department.id,
        }
        
        form = HospitalizationForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "main_symptom": "Fever",
            "additional_symptoms" : "Fatigue",
            "department_id" : self.department.id,
        }
        
        form = HospitalizationForm(data)
        self.assertTrue(form.is_valid())
        
        hospitalization = form.save(commit=False)
        hospitalization.created_by = self.user
        hospitalization.patient = self.patient
        hospitalization.department = self.department
        hospitalization.save()     
        self.assertIsInstance(hospitalization, Hospitalization)