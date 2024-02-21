from django.test import TestCase

from department.models import Department, Hospitalization
from main.models import User
from patient.models import Patient
from scales.forms import BodyMassIndexForm, GlasgowComaScaleForm, NewsScaleForm, NortonScaleForm, PainScaleForm
from scales.models import BodyMassIndex, GlasgowComaScale, NewsScale, NortonScale, PainScale

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
            "body_height" : 70,
            "body_weight" : 100,
        }
        
        form = BodyMassIndexForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            "body_height" : "ha",
            #"body_weight" : 100,
        }
        form = BodyMassIndexForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "body_height" : 70,
            "body_weight" : 100,
        }
        form = BodyMassIndexForm(data)
        self.assertTrue(form.is_valid())
        
        bmi = form.save(commit=False)
        bmi.created_by = self.user
        bmi.hospitalization = self.hospitalization
        bmi.save()     
        self.assertIsInstance(bmi, BodyMassIndex)
    
    def test_form_labels(self):
        form = BodyMassIndexForm()
        self.assertTrue(form.fields["body_height"].label == "Body height in cenimeters")
        self.assertTrue(form.fields["body_weight"].label == "Body weight in kilograms")

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
            "eye_response" : "4",
            "verbal_response": "5",
            "motor_response": "5",
        }
        form = GlasgowComaScaleForm(data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        data = {
            "eye_response" : "4",
            #"verbal_response": "5",
            "motor_response": "5",
        }
        form = GlasgowComaScaleForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "eye_response" : "4",
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
        
    def test_form_labels(self):
        form = GlasgowComaScaleForm()
        self.assertTrue(form.fields["eye_response"].label == "Best eye response")
        self.assertTrue(form.fields["verbal_response"].label == "Best verbal response")
        self.assertTrue(form.fields["motor_response"].label == "Best motor response")

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
            "respiratory_rate" : 20,
            "oxygen_saturation" : 100,
            "is_on_oxygen" : False,
            "aecopd_state" : False,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 80,
            "heart_rate" : 66,
            "level_of_consciousness" : "awake"
        }
        form = NewsScaleForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            "respiratory_rate" : 20,
            "oxygen_saturation" : 100,
            "is_on_oxygen" : False,
            "aecopd_state" : False,
            #"temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 80,
            "heart_rate" : 66,
            #"level_of_consciousness" : "awake"
        }
        form = NewsScaleForm(data)
        self.assertFalse(form.is_valid())  
    
    def test_clean_method_invalid_blood_pressure(self):
        data = {
            "respiratory_rate" : 20,
            "oxygen_saturation" : 100,
            "is_on_oxygen" : False,
            "aecopd_state" : False,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 80,
            "diastolic_blood_pressure" : 100,
            "heart_rate" : 66,
            "level_of_consciousness" : "awake"
        }
        form = NewsScaleForm(data)
        self.assertFalse(form.is_valid())
          

    
    def test_save_method(self):
        data = {
            "respiratory_rate" : 20,
            "oxygen_saturation" : 100,
            "is_on_oxygen" : False,
            "aecopd_state" : False,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 80,
            "heart_rate" : 66,
            "level_of_consciousness" : "awake"
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
            "physical_condition": "4",
            "mental_condition" : "4",
            "activity" : "4",
            "mobility" : "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        data = {
            #"physical_condition": "4",
            "mental_condition" : "4",
            "activity" : "4",
            #"mobility" : "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertFalse(form.is_valid())
        
    def test_save_method(self):
        data = {
            "physical_condition": "4",
            "mental_condition" : "4",
            "activity" : "4",
            "mobility" : "4",
            "incontinence": "4",
        }
        form = NortonScaleForm(data)
        self.assertTrue(form.is_valid())
        
        norton = form.save(commit=False)
        norton.created_by = self.user
        norton.hospitalization = self.hospitalization
        norton.save()
        
        self.assertIsInstance(norton, NortonScale)
    
    def test_form_labels(self):
        form = NortonScaleForm()
        self.assertTrue(form.fields["physical_condition"].label == "Physical condition")
        self.assertTrue(form.fields["mental_condition"].label == "Mental condition")
        self.assertTrue(form.fields["activity"].label == "Activity")
        self.assertTrue(form.fields["mobility"].label == "Mobility")
        self.assertTrue(form.fields["incontinence"].label == "Incontinence")
        
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
            "pain_level" : "0",
            "pain_comment": "No Pain"
        }
        form = PainScaleForm(data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        data = {
            #"pain_level" : "0",
            "pain_comment": "No Pain"
        }
        form = PainScaleForm(data)
        self.assertFalse(form.is_valid())  
        
    def test_save_method(self):
        data = {
            "pain_level" : "0",
            "pain_comment": "No Pain"
        }
        form = PainScaleForm(data)
        self.assertTrue(form.is_valid())
        
        pain = form.save(commit=False)
        pain.created_by = self.user
        pain.hospitalization = self.hospitalization
        pain.save()
        
        self.assertIsInstance(pain, PainScale)
    
    def test_form_labels(self):
        form = PainScaleForm()
        self.assertTrue(form.fields["pain_level"].label == "Pain level")
        self.assertTrue(form.fields["pain_comment"].label == "Pain comment")
        