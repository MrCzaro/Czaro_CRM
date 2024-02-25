from django.test import TestCase
from django.urls import reverse

from main.models import User

from department.models import Consultation, Department, Hospitalization, Observation, VitalSigns
from patient.models import Patient

class CreatePatientConsultationViewTest(TestCase):
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
        response = self.client.get(reverse("department:consultation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-consultation-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("department:consultation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:consultation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_consultation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:consultation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    def test_form_submission_valid_data(self):
        data = {
            "consultation_name" : "Test Consultation",
            "consultation" : "This is content for a test."
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:consultation_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(Consultation.objects.count(), 1) 
        
    def test_form_submission_invalid_data(self):
        data = {
            "consultation_name" : "",
            #"consultation" : "This is content for a test."
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:consultation_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_consultation_form.html")
        self.assertEqual(Consultation.objects.count(), 0) 
        
class UpdatePatientConsultationViewTest(TestCase):
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
        cls.consultation = Consultation.objects.create(
            hospitalization = cls.hospitalization,
            consultation_name = "Test Consultation",
            consultation = "This is content for a test.",
            created_by = cls.user
        )
    def test_authentication_required(self):
        response = self.client.get(reverse("department:consultation_update", args=[self.patient.id, self.hospitalization.id, self.consultation.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-consultation-edit/{self.consultation.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("department:consultation_update", args=[self.patient.id, self.hospitalization.id, self.consultation.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:consultation_update", args=[self.patient.id, self.hospitalization.id, self.consultation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_consultation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:consultation_update", args=[self.patient.id, self.hospitalization.id, self.consultation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "consultation_name" : "Test Consultation Updated",
            "consultation" : "This is content for a test - Updated."
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:consultation_update", args=[self.patient.id, self.hospitalization.id, self.consultation.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_consultation = Consultation.objects.get(id=self.consultation.id)
        self.assertEqual(updated_consultation.consultation_name, "Test Consultation Updated")
        self.assertEqual(updated_consultation.consultation, "This is content for a test - Updated.")
        
class CreatePatientObservationViewTest(TestCase):
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
        response = self.client.get(reverse("department:observation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-observation-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("department:observation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:observation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_observation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:observation_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    def test_form_submission_valid_data(self):
        data = {
            "observation" : "This is content for a test."
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:observation_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(Observation.objects.count(), 1) 
        
    def test_form_submission_invalid_data(self):
        data = {}
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:observation_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_observation_form.html")
        self.assertEqual(Observation.objects.count(), 0) 
        
class UpdatePatientObservationViewTest(TestCase):
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
        cls.observation=Observation.objects.create(
            hospitalization=cls.hospitalization,
            observation="Observation 1",
            created_by = cls.user,
        )
    def test_authentication_required(self):
        response = self.client.get(reverse("department:observation_update", args=[self.patient.id, self.hospitalization.id, self.observation.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-observation-edit/{self.observation.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("department:observation_update", args=[self.patient.id, self.hospitalization.id, self.observation.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:observation_update", args=[self.patient.id, self.hospitalization.id, self.observation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_observation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:observation_update", args=[self.patient.id, self.hospitalization.id, self.observation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "observation" : "Updated observation.",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:observation_update", args=[self.patient.id, self.hospitalization.id, self.observation.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_observation = Observation.objects.get(id=self.observation.id)
        self.assertEqual(updated_observation .observation, "Updated observation.")
        
class CreateVitalSignsViewTest(TestCase):
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
        response = self.client.get(reverse("department:vitals_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/vital-signs-add/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("department:vitals_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:vitals_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:vitals_create", args=[self.patient.id, self.hospitalization.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    def test_form_submission_valid_data(self):
        data = {
            "respiratory_rate" : 20,
            "oxygen_saturation" : 99,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 70,
            "heart_rate" : 64,
        }
        
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:vitals_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        self.assertEqual(VitalSigns.objects.count(), 1) 
        
    def test_form_submission_invalid_data(self):
        data = {
            "respiratory_rate" : -20,
            "oxygen_saturation" : 99,
            "temperature" : 36.6,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 70,
            #"heart_rate" : 64,
        }
        
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:vitals_create", args=[self.patient.id, self.hospitalization.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")
        self.assertEqual(VitalSigns.objects.count(), 0) 
        
class UpdateVitalSignsViewTest(TestCase):
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
        cls.vital = VitalSigns.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            respiratory_rate=20,
            oxygen_saturation=100,
            temperature=37.2,
            systolic_blood_pressure=120,
            diastolic_blood_pressure=70,
            heart_rate=88,
        )
    def test_authentication_required(self):
        response = self.client.get(reverse("department:vitals_update", args=[self.patient.id, self.hospitalization.id, self.vital.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/vital-signs-edit/{self.vital.id}/")
    
    def access_denied_for_secretaries(self):
        self.client.login(username="testsecretary@admin.com", password="secretarypassword")
        response = self.client.get(reverse("department:vitals_update", args=[self.patient.id, self.hospitalization.id, self.vital.id]))
        self.assertRedirects(response,reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")
        
        
    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:vitals_update", args=[self.patient.id, self.hospitalization.id, self.vital.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:vitals_update", args=[self.patient.id, self.hospitalization.id, self.vital.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)
        
    
    def test_form_submission(self):
        data = {
            "respiratory_rate" : 18,
            "oxygen_saturation" : 99,
            "temperature" : 37.2,
            "systolic_blood_pressure" : 120,
            "diastolic_blood_pressure" : 70,
            "heart_rate" : 64,
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:vitals_update", args=[self.patient.id, self.hospitalization.id, self.vital.id]),data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:hospitalization", args=[self.hospitalization.id]))
        updated_vitals = VitalSigns.objects.get(id=self.vital.id)
        self.assertEqual(updated_vitals.respiratory_rate, 18)
        self.assertEqual(updated_vitals.oxygen_saturation, 99)
        self.assertEqual(updated_vitals.heart_rate, 64)
        
    

        
