from django.test import TestCase
from django.urls import reverse

from main.models import User
from department.models import Department, Hospitalization
from patient.models import Patient
from scales.models import BodyMassIndex, NortonScale, GlasgowComaScale, NewsScale, PainScale

class AccessDeniedViewTest(TestCase):
    def test_access_denied(self):
        response = self.client.get(reverse("access_denied"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "access_denied.html")
    
class CreatePatientBmiViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:bmi_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/bmi-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:bmi_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:bmi_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:bmi_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    def test_form_submission_valid_data(self):
        data = {
            "body_height": 170,
            "body_weight": 70, 
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:bmi_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(BodyMassIndex.objects.count(), 1) 

        
    def test_form_submission_invalid_data(self):
        data = {
            "body_height": "ha",
            "body_weight": 70, 
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:bmi_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")
        self.assertEqual(BodyMassIndex.objects.count(), 0) 
        
class UpdatePatientBmiViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        cls.body_mass_index = BodyMassIndex.objects.create(
            hospitalization = cls.hospitalization,
            created_by=cls.user,
            body_height=170,
            body_weight=70,
        )
        
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:bmi_update", args=[self.patient.id, self.hospitalization.id, self.body_mass_index.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/bmi-edit/{self.body_mass_index.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:bmi_update", args=[self.patient.id, self.hospitalization.id, self.body_mass_index.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:bmi_update", args=[self.patient.id, self.hospitalization.id, self.body_mass_index.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:bmi_update", args=[self.patient.id, self.hospitalization.id, self.body_mass_index.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "body_height": 170,
            "body_weight": 80, 
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:bmi_update", args=[self.patient.id, self.hospitalization.id, self.body_mass_index.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_bmi = BodyMassIndex.objects.get(id=self.body_mass_index.id)
        self.assertEqual(updated_bmi.body_weight, 80)
        
class CreateGlasgowScaleViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:glasgow_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/glasgow-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:glasgow_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:glasgow_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:glasgow_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    def test_form_submission_valid_data(self):
        data = {
            "eye_response" : "4",
            "verbal_response" : "3",
            "motor_response" : "5",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:glasgow_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(GlasgowComaScale.objects.count(), 1) 

        
    def test_form_submission_invalid_data(self):
        data = {
            "eye_response" : "ha",
            "verbal_response" : "3",
            "motor_response" : "5",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:glasgow_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")
        self.assertEqual(GlasgowComaScale.objects.count(), 0) 
        
        
class UpdateGlasgowScaleViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        cls.glasgow = GlasgowComaScale.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            eye_response="4",
            verbal_response="3",
            motor_response="5",
        )
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:glasgow_update", args=[self.patient.id, self.hospitalization.id, self.glasgow.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/glasgow-edit/{self.glasgow.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:glasgow_update", args=[self.patient.id, self.hospitalization.id, self.glasgow.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:glasgow_update", args=[self.patient.id, self.hospitalization.id, self.glasgow.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:glasgow_update", args=[self.patient.id, self.hospitalization.id, self.glasgow.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "eye_response" : "4",
            "verbal_response" : "5",
            "motor_response" : "6",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:glasgow_update", args=[self.patient.id, self.hospitalization.id, self.glasgow.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_glasgow = GlasgowComaScale.objects.get(id=self.glasgow.id)
        self.assertEqual(updated_glasgow.verbal_response, "5")
        self.assertEqual(updated_glasgow.motor_response, "6")
        
class CreateNewsScaleViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:news_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/news-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:news_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:news_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:news_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
    
        
    def test_form_submission_valid_data(self):
        data = {
            "respiratory_rate" : 20,
            "oxygen_saturation" : 99,
            "is_on_oxygen" : False,
            "aecopd_state" : False,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 70,
            "heart_rate" : 64,
            "level_of_consciousness" : "awake"
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:news_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(NewsScale.objects.count(), 1) 

        
    def test_form_submission_invalid_data(self):
        data = {
            "respiratory_rate" : "one",
            "oxygen_saturation" : 99,
            "is_on_oxygen" : False,
            "aecopd_state" : False,
            #"temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 70,
            "heart_rate" : 64,
            "level_of_consciousness" : "bad"
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:news_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")
        self.assertEqual(NewsScale.objects.count(), 0) 
        
class UpdateNewsScaleViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        cls.news = NewsScale(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            respiratory_rate=20,
            oxygen_saturation=99,
            is_on_oxygen=False,
            aecopd_state=False,
            temperature=36.6,
            systolic_blood_pressure=120,
            diastolic_blood_pressure=70,
            heart_rate=64,
            level_of_consciousness="awake"        
        )
        cls.news.save()
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:news_update", args=[self.patient.id, self.hospitalization.id, self.news.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/news-edit/{self.news.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:news_update", args=[self.patient.id, self.hospitalization.id, self.news.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:news_update", args=[self.patient.id, self.hospitalization.id, self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:news_update", args=[self.patient.id, self.hospitalization.id, self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "respiratory_rate" : 20,
            "oxygen_saturation" : 89,
            "is_on_oxygen" : True,
            "aecopd_state" : False,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 70,
            "heart_rate" : 64,
            "level_of_consciousness" : "unresponsive"
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:news_update", args=[self.patient.id, self.hospitalization.id, self.news.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_news = NewsScale.objects.get(id=self.news.id)
        self.assertEqual(updated_news.level_of_consciousness, "unresponsive")
        self.assertEqual(updated_news.is_on_oxygen, True)
        self.assertEqual(updated_news.oxygen_saturation, 89)
        
class CreateNortonScaleViewTest(TestCase):
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:norton_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/norton-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:norton_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:norton_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:norton_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
    
        
    def test_form_submission_valid_data(self):
        data = {
            "physical_condition" : "4",
            "mental_condition" : "4",
            "activity" : "4",
            "mobility" : "4",
            "incontinence" : "4", 
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:norton_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(NortonScale.objects.count(), 1) 

        
    def test_form_submission_invalid_data(self):
        data = {
            "physical_condition" : "ha",
            "mental_condition" : "4",
            "activity" : "4",
            #"mobility" : "4",
            "incontinence" : "4", 
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:norton_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")
        self.assertEqual(NortonScale.objects.count(), 0) 
        
class UpdateNortonScaleViewTest(TestCase):
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
        cls.norton = NortonScale.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            physical_condition="4",
            mental_condition="4",
            activity="4",
            mobility="4",
            incontinence="4",        
        )
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:norton_update", args=[self.patient.id, self.hospitalization.id, self.norton.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/norton-edit/{self.norton.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:norton_update", args=[self.patient.id, self.hospitalization.id, self.norton.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:norton_update", args=[self.patient.id, self.hospitalization.id, self.norton.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:norton_update", args=[self.patient.id, self.hospitalization.id, self.norton.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "physical_condition" : "3",
            "mental_condition" : "4",
            "activity" : "1",
            "mobility" : "1",
            "incontinence" : "1", 
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:norton_update", args=[self.patient.id, self.hospitalization.id, self.norton.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_norton = NortonScale.objects.get(id=self.norton.id)
        self.assertEqual(updated_norton.physical_condition, "3")
        self.assertEqual(updated_norton.activity, "1")
        self.assertEqual(updated_norton.mobility, "1")
        
class CreatePainScaleViewTest(TestCase):
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.secretary = User.objects.create_user(
            first_name="SecretaryTest",
            last_name="User",
            email="testsecretary@admin.com",
            password="secretarypassword",
            profession="secretaries",
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
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:pain_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/pain-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:pain_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:pain_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:pain_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
    
        
    def test_form_submission_valid_data(self):
        data = {
            "pain_level" : "5",
            "pain_comment" : "",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:pain_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(PainScale.objects.count(), 1) 

        
    def test_form_submission_invalid_data(self):
        data = {
            "pain_level" : "haha",
            "pain_comment" : "",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:pain_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")
        self.assertEqual(PainScale.objects.count(), 0) 
        
class UpdatePainScaleViewTest(TestCase):
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
        cls.pain = PainScale.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            pain_level="5",
            pain_comment="",
        )
        
    def test_authentication_required(self):
        response = self.client.get(reverse("scales:pain_update", args=[self.patient.id, self.hospitalization.id, self.pain.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/scale/{self.patient.id}/{self.hospitalization.id}/pain-edit/{self.pain.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("scales:pain_update", args=[self.patient.id, self.hospitalization.id, self.pain.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:pain_update", args=[self.patient.id, self.hospitalization.id, self.pain.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("scales:pain_update", args=[self.patient.id, self.hospitalization.id, self.pain.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "pain_level" : "8",
            "pain_comment" : "Acute",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("scales:pain_update", args=[self.patient.id, self.hospitalization.id, self.pain.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_pain = PainScale.objects.get(id=self.pain.id)
        self.assertEqual(updated_pain.pain_level, "8")
        self.assertEqual(updated_pain.pain_comment, "Acute")
        

    
        