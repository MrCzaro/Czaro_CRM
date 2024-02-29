from django.test import TestCase

from department.forms import (
    ConsultationForm,
    DepartmentForm,
    DischargeForm,
    HospitalizationForm,
    ObservationForm,
    TransferPatientForm,
    VitalSignsForm,
)
from department.models import (
    Consultation,
    Department,
    Hospitalization,
    Observation,
    VitalSigns,
)
from patient.models import Patient
from main.models import User


class DepartmentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_admin = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.user_nurse = User.objects.create_user(
            first_name="NurseTest",
            last_name="User",
            email="testnurse@admin.com",
            password="nursepassword",
            profession="nurses",
        )

    def test_form_initialization(self):
        form = DepartmentForm()
        self.assertIsInstance(form, DepartmentForm)

    def test_valid_form(self):
        data = {
            "name": "Test Department",
            "description": "Test Description Department",
        }

        form = DepartmentForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            # "name" : "Test Department",
            "description": "Test Description Department",
        }
        form = DepartmentForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "name": "Test Department without Description",
        }
        form = DepartmentForm(data)
        self.assertFalse(form.is_valid())

    def test_clean_method(self):
        # Test clean method - user with admin profession:
        data = {
            "name": "Test Department",
            "description": "Test Description Department",
        }
        form = DepartmentForm(data, initial={"created_by": self.user_admin})
        self.assertTrue(form.is_valid())

        # Test clean method - user without admin profession:
        data = {
            "name": "Test Department",
            "description": "Test Description Department",
        }
        form = DepartmentForm(data, initial={"created_by": self.user_nurse})
        self.assertFalse(form.is_valid())

    def test_save_method(self):
        data = {
            "name": "Test Department",
            "description": "Test Description Department",
        }
        form = DepartmentForm(data)
        self.assertTrue(form.is_valid())

        department = form.save(commit=False)
        department.created_by = self.user_admin
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
            created_by=cls.user,
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
            created_by=cls.user,
        )
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )

    def test_form_initialization(self):
        form = ConsultationForm()
        self.assertIsInstance(form, ConsultationForm)

    def test_valid_form(self):
        data = {
            "consultation_name": "Test Name of Consultation",
            "consultation": "Test Consulation",
        }

        form = ConsultationForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            # "consultation_name": "Test Name of Consultation",
            "consultation": "Test Consulation",
        }
        form = ConsultationForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "consultation_name": "Test Name of Consultation",
            # "consultation": "Test Consulation",
        }
        form = ConsultationForm(data)
        self.assertFalse(form.is_valid())

    def test_consultation_name_label(self):
        form = ConsultationForm()
        self.assertEqual(form.fields["consultation_name"].label, "Name of Consultation")

    def test_consultation_label(self):
        form = ConsultationForm()
        self.assertEqual(form.fields["consultation"].label, "Description")

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
            created_by=cls.user,
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
            created_by=cls.user,
        )
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )

    def test_form_initialization(self):
        form = ObservationForm()
        self.assertIsInstance(form, ObservationForm)

    def test_valid_form(self):
        data = {
            "observation": "Test Observation",
        }

        form = ObservationForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            # "observation": "Test Observation",
        }
        form = ObservationForm(data)
        self.assertFalse(form.is_valid())

    def test_observation_label(self):
        form = ObservationForm()
        self.assertEqual(form.fields["observation"].label, "Patient observation")

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
            created_by=cls.user,
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
            created_by=cls.user,
        )

    def test_form_initialization(self):
        form = HospitalizationForm()
        self.assertIsInstance(form, HospitalizationForm)

    def test_valid_form(self):
        data = {
            "main_symptom": "Fever",
            "additional_symptoms": "Fatigue",
            "department_id": self.department.id,
        }

        form = HospitalizationForm(data)
        self.assertTrue(form.is_valid())

        data = {
            "main_symptom": "Fever",
            "department_id": self.department.id,
        }

        form = HospitalizationForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            # "main_symptom": "Fever",
            "additional_symptoms": "Fatigue",
            "department_id": self.department.id,
        }

        form = HospitalizationForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "main_symptom": "Fever",
            "additional_symptoms": "Fatigue",
            # "department_id" : self.department.id,
        }

        form = HospitalizationForm(data)
        self.assertFalse(form.is_valid())

    def test_main_symptom_label(self):
        form = HospitalizationForm()
        self.assertEqual(form.fields["main_symptom"].label, "Main symptom")

    def test_additional_symptoms_label(self):
        form = HospitalizationForm()
        self.assertEqual(
            form.fields["additional_symptoms"].label, "Additional symptoms"
        )

    def test_save_method(self):
        data = {
            "main_symptom": "Fever",
            "additional_symptoms": "Fatigue",
            "department_id": self.department.id,
        }

        form = HospitalizationForm(data)
        self.assertTrue(form.is_valid())

        hospitalization = form.save(commit=False)
        hospitalization.created_by = self.user
        hospitalization.patient = self.patient
        hospitalization.department = self.department
        hospitalization.save()
        self.assertIsInstance(hospitalization, Hospitalization)


class TransferPatientFormTest(TestCase):
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
            created_by=cls.user,
        )

    def test_form_initialization(self):
        form = TransferPatientForm()
        self.assertIsInstance(form, TransferPatientForm)

    def test_valid_form(self):
        data = {
            "department": self.department,
        }

        form = TransferPatientForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "department": "Fake Department",
        }
        form = TransferPatientForm(data)
        self.assertFalse(form.is_valid())

        data = {}
        form = TransferPatientForm(data)
        self.assertFalse(form.is_valid())

    def test_empty_label(self):
        form = TransferPatientForm()
        self.assertEqual(form.fields["department"].empty_label, "Select Department")

    def test_field_label(self):
        form = TransferPatientForm()
        self.assertEqual(form.fields["department"].label, "Transfer to Department")

    def test_department_queryset(self):
        form = TransferPatientForm()
        self.assertQuerySetEqual(
            form.fields["department"].queryset,
            Department.objects.all(),
            transform=lambda x: x,
        )


class DischargeFormTest(TestCase):
    def test_form_initialization(self):
        form = DischargeForm()
        self.assertIsInstance(form, DischargeForm)

    def test_valid_form(self):
        data = {
            "discharge_date": "2024-02-17",
            "discharge_time": "15:20",
        }
        form = DischargeForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = DischargeForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("discharge_date" in form.errors)
        self.assertTrue("discharge_time" in form.errors)

        # Test wrong input

        data = {
            "discharge_date": "2024-02-17",
            "discharge_time": "3PM",
        }
        form = DischargeForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("discharge_time" in form.errors)

        data = {
            "discharge_date": "Friday",
            "discharge_time": "15:20",
        }
        form = DischargeForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue("discharge_date" in form.errors)

    def test_dicharge_date_label(self):
        form = DischargeForm()
        self.assertEqual(form.fields["discharge_date"].label, "Discharge Date")

    def test_dicharge_time_label(self):
        form = DischargeForm()
        self.assertEqual(form.fields["discharge_time"].label, "Discharge Time")


class VitalSignsFormTest(TestCase):
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
            created_by=cls.user,
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
            created_by=cls.user,
        )
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.patient,
            department=cls.department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )

    def test_form_initialization(self):
        form = VitalSignsForm()
        self.assertIsInstance(form, VitalSignsForm)

    def test_valid_form(self):
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
        }

        form = VitalSignsForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = VitalSignsForm(data)
        self.assertFalse(form.is_valid())

        # Test missing fields
        data = {
            # "respiratory_rate" : 20,
            # "oxygen_saturation" : 100,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
        }
        form = VitalSignsForm(data)
        self.assertFalse(form.is_valid())

        # Test wrong input
        data = {
            "respiratory_rate": "ha",
            "oxygen_saturation": 100,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
        }
        form = VitalSignsForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "temperature": 36.6,
            "systolic_blood_pressure": 80,
            "diastolic_blood_pressure": 180,  # diastolic blood pressure should be always lower than systolic
            "heart_rate": 66,
        }

        form = VitalSignsForm(data)
        self.assertFalse(form.is_valid())

    def test_respiratory_rate_label(self):
        form = VitalSignsForm()
        self.assertEqual(form.fields["respiratory_rate"].label, "Respiratory rate")

    def test_oxygen_saturation_label(self):
        form = VitalSignsForm()
        self.assertEqual(
            form.fields["oxygen_saturation"].label, "Oxygen saturation level"
        )

    def test_temperature_rate_label(self):
        form = VitalSignsForm()
        self.assertEqual(form.fields["temperature"].label, "Body temperature")

    def test_systolic_blood_pressure_label(self):
        form = VitalSignsForm()
        self.assertEqual(
            form.fields["systolic_blood_pressure"].label, "Systolic blood presurre"
        )

    def test_diastolic_blood_pressure_label(self):
        form = VitalSignsForm()
        self.assertEqual(
            form.fields["diastolic_blood_pressure"].label, "Diastolic blood pressure"
        )

    def test_heart_rate_label(self):
        form = VitalSignsForm()
        self.assertEqual(form.fields["heart_rate"].label, "Heart Rate")

    def test_save_method(self):
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
        }

        form = VitalSignsForm(data)
        self.assertTrue(form.is_valid())

        vital = form.save(commit=False)
        vital.created_by = self.user
        vital.hospitalization = self.hospitalization
        vital.save()
        self.assertIsInstance(vital, VitalSigns)
