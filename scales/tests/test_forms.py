from django.test import TestCase

from department.models import Department, Hospitalization
from main.models import User
from patient.models import Patient
from scales.forms import (
    BodyMassIndexForm,
    GlasgowComaScaleForm,
    NewsScaleForm,
    NortonScaleForm,
    PainScaleForm,
)
from scales.models import (
    BodyMassIndex,
    GlasgowComaScale,
    NewsScale,
    NortonScale,
    PainScale,
)


class BodyMassIndexFormTest(TestCase):
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
        form = BodyMassIndexForm()
        self.assertIsInstance(form, BodyMassIndexForm)

    def test_valid_form(self):
        data = {
            "body_height": 70,
            "body_weight": 100,
        }

        form = BodyMassIndexForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = BodyMassIndexForm(data)
        self.assertFalse(form.is_valid())

        # Test missing fields
        data = {
            "body_weight": 100,
        }
        form = BodyMassIndexForm(data)
        self.assertFalse(form.is_valid())

        # Test wrong input
        data = {
            "body_height": "ha",
            "body_weight": 100,
        }
        form = BodyMassIndexForm(data)
        self.assertFalse(form.is_valid())

    def test_body_height_label(self):
        form = BodyMassIndexForm()
        self.assertEqual(form.fields["body_height"].label, "Body height in cenimeters")

    def test_body_weight_label(self):
        form = BodyMassIndexForm()
        self.assertEqual(form.fields["body_weight"].label, "Body weight in kilograms")

    def test_save_method(self):
        data = {
            "body_height": 70,
            "body_weight": 100,
        }
        form = BodyMassIndexForm(data)
        self.assertTrue(form.is_valid())

        bmi = form.save(commit=False)
        bmi.created_by = self.user
        bmi.hospitalization = self.hospitalization
        bmi.save()
        self.assertIsInstance(bmi, BodyMassIndex)


class GlasgowComaScaleFormTest(TestCase):
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
        form = GlasgowComaScaleForm()
        self.assertIsInstance(form, GlasgowComaScaleForm)

    def test_valid_form(self):
        data = {
            "eye_response": "4",
            "verbal_response": "5",
            "motor_response": "5",
        }
        form = GlasgowComaScaleForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = GlasgowComaScaleForm(data)

        # Test wrong input
        data = {
            "eye_response": 10,
            "verbal_response": "5",
            "motor_response": "5",
        }
        form = GlasgowComaScaleForm(data)

        # Test missing fields
        data = {
            "eye_response": "4",
            # "verbal_response": "5",
            "motor_response": "5",
        }
        form = GlasgowComaScaleForm(data)
        self.assertFalse(form.is_valid())

    def test_eye_response_label(self):
        form = GlasgowComaScaleForm()
        self.assertEqual(form.fields["eye_response"].label, "Best eye response")

    def test_verbal_response_label(self):
        form = GlasgowComaScaleForm()
        self.assertEqual(form.fields["verbal_response"].label, "Best verbal response")

    def test_motor_response_label(self):
        form = GlasgowComaScaleForm()
        self.assertEqual(form.fields["motor_response"].label, "Best motor response")

    def test_save_method(self):
        data = {
            "eye_response": "4",
            "verbal_response": "5",
            "motor_response": "5",
        }
        form = GlasgowComaScaleForm(data)
        self.assertTrue(form.is_valid())

        glasgow = form.save(commit=False)
        glasgow.created_by = self.user
        glasgow.hospitalization = self.hospitalization
        glasgow.save()

        self.assertIsInstance(glasgow, GlasgowComaScale)


class NewsScaleFormTest(TestCase):
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
        form = NewsScaleForm()
        self.assertIsInstance(form, NewsScaleForm)

    def test_valid_form(self):
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "is_on_oxygen": False,
            "aecopd_state": False,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
            "level_of_consciousness": "awake",
        }
        form = NewsScaleForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = NewsScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test wrong input
        data = {
            "respiratory_rate": "ha",
            "oxygen_saturation": 100,
            "is_on_oxygen": False,
            "aecopd_state": False,
            "temperature": 500,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
            "level_of_consciousness": "awake",
        }
        form = NewsScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test missing fields
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "is_on_oxygen": False,
            "aecopd_state": False,
            # "temperature" : 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
            # "level_of_consciousness" : "awake"
        }
        form = NewsScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test wrong blood pressure - clean method
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "is_on_oxygen": False,
            "aecopd_state": False,
            "temperature": 36.6,
            "systolic_blood_pressure": 80,
            "diastolic_blood_pressure": 100,
            "heart_rate": 66,
            "level_of_consciousness": "awake",
        }
        form = NewsScaleForm(data)
        self.assertFalse(form.is_valid())

    def test_respiratory_rate_label(self):
        form = NewsScaleForm()
        self.assertEqual(form.fields["respiratory_rate"].label, "Respiratory rate")

    def test_oxygen_saturation_label(self):
        form = NewsScaleForm()
        self.assertEqual(
            form.fields["oxygen_saturation"].label, "Oxygen saturation level"
        )

    def test_is_on_oxygen_label(self):
        form = NewsScaleForm()
        self.assertEqual(form.fields["is_on_oxygen"].label, "Oxygen supplementation")

    def test_aecopd_state_label(self):
        form = NewsScaleForm()
        self.assertEqual(
            form.fields["aecopd_state"].label,
            "Is the patient in Acute exacebrations of chronic obstructive pulmonary disease state",
        )

    def test_temperature_label(self):
        form = NewsScaleForm()
        self.assertEqual(form.fields["temperature"].label, "Body temperature")

    def test_systolic_blood_pressure_label(self):
        form = NewsScaleForm()
        self.assertEqual(
            form.fields["systolic_blood_pressure"].label, "Systolic blood presurre"
        )

    def test_diastolic_blood_pressure_label(self):
        form = NewsScaleForm()
        self.assertEqual(
            form.fields["diastolic_blood_pressure"].label, "Diastolic blood pressure"
        )

    def test_heart_rate_label(self):
        form = NewsScaleForm()
        self.assertEqual(form.fields["heart_rate"].label, "Heart Rate")

    def test_level_of_consciousness_label(self):
        form = NewsScaleForm()
        self.assertEqual(
            form.fields["level_of_consciousness"].label, "Level of consciousness"
        )

    def test_save_method(self):
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 100,
            "is_on_oxygen": False,
            "aecopd_state": False,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 80,
            "heart_rate": 66,
            "level_of_consciousness": "awake",
        }
        form = NewsScaleForm(data)
        self.assertTrue(form.is_valid())

        news = form.save(commit=False)
        news.created_by = self.user
        news.hospitalization = self.hospitalization
        news.save()

        self.assertIsInstance(news, NewsScale)


class NortonSacleFormTest(TestCase):
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
        form = NortonScaleForm()
        self.assertIsInstance(form, NortonScaleForm)

    def test_valid_form(self):
        data = {
            "physical_condition": "4",
            "mental_condition": "4",
            "activity": "4",
            "mobility": "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = NortonScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test wrong input
        data = {
            "physical_condition": 15,
            "mental_condition": "ha",
            "activity": "4",
            "mobility": "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test missing fields
        data = {
            # "physical_condition": "4",
            "mental_condition": "4",
            "activity": "4",
            # "mobility" : "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertFalse(form.is_valid())

    def test_physical_condition_label(self):
        form = NortonScaleForm()
        self.assertEqual(form.fields["physical_condition"].label, "Physical condition")

    def test_mental_condition_label(self):
        form = NortonScaleForm()
        self.assertEqual(form.fields["mental_condition"].label, "Mental condition")

    def test_activity_label(self):
        form = NortonScaleForm()
        self.assertEqual(form.fields["activity"].label, "Activity")

    def test_mobility_label(self):
        form = NortonScaleForm()
        self.assertEqual(form.fields["mobility"].label, "Mobility")

    def test_incontinence_label(self):
        form = NortonScaleForm()
        self.assertEqual(form.fields["incontinence"].label, "Incontinence")

    def test_save_method(self):
        data = {
            "physical_condition": "4",
            "mental_condition": "4",
            "activity": "4",
            "mobility": "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertTrue(form.is_valid())

        norton = form.save(commit=False)
        norton.created_by = self.user
        norton.hospitalization = self.hospitalization
        norton.save()

        self.assertIsInstance(norton, NortonScale)


class PainScaleFormTest(TestCase):
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
        form = PainScaleForm()
        self.assertIsInstance(form, PainScaleForm)

    def test_valid_form(self):
        data = {"pain_level": "0", "pain_comment": "No Pain"}
        form = PainScaleForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test empty form
        data = {}
        form = PainScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test wrong input
        data = {"pain_level": 11, "pain_comment": "No Pain"}
        form = PainScaleForm(data)
        self.assertFalse(form.is_valid())

        # Test missing fields
        data = {
            # "pain_level" : "0",
            "pain_comment": "No Pain"
        }
        form = PainScaleForm(data)
        self.assertFalse(form.is_valid())

    def test_pain_level_label(self):
        form = PainScaleForm()
        self.assertEqual(form.fields["pain_level"].label, "Pain level")

    def test_pain_comment_label(self):
        form = PainScaleForm()
        self.assertEqual(form.fields["pain_comment"].label, "Pain comment")

    def test_save_method(self):
        data = {"pain_level": "0", "pain_comment": "No Pain"}
        form = PainScaleForm(data)
        self.assertTrue(form.is_valid())

        pain = form.save(commit=False)
        pain.created_by = self.user
        pain.hospitalization = self.hospitalization
        pain.save()

        self.assertIsInstance(pain, PainScale)
