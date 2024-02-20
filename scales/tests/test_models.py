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
        self.assertIsNotNone(self.glasgow.created_at)
        self.assertIsNotNone(self.glasgow.modified_at)
        self.assertLessEqual(self.glasgow.created_at, self.glasgow.modified_at)
        
    def test_eye_response_label(self):
        field_label = self.glasgow._meta.get_field("eye_response").verbose_name
        self.assertEqual(field_label, "eye response")
        
    def test_motor_response_label(self):
        field_label = self.glasgow._meta.get_field("motor_response").verbose_name
        self.assertEqual(field_label, "motor response")
        
    def test_verbal_response_label(self):
        field_label = self.glasgow._meta.get_field("verbal_response").verbose_name
        self.assertEqual(field_label, "verbal response")
        
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
        
class NortonScaleModelTest(TestCase):
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
        cls.norton = NortonScale.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            physical_condition="4",
            mental_condition="4",
            activity="4",
            mobility="4",
            incontinence="4",        
        )
    
    def test_valid_norton_scale(self):
        self.assertEqual(self.norton.physical_condition, "4")
        self.assertEqual(self.norton.mental_condition, "4")
        self.assertEqual(self.norton.activity,"4")
        self.assertEqual(self.norton.mobility, "4")
        self.assertEqual(self.norton.incontinence, "4")
        self.assertEqual(self.norton.created_by, self.user)
        self.assertIsNotNone(self.norton.created_at)
        self.assertIsNotNone(self.norton.modified_at)
        self.assertLessEqual(self.norton.created_at, self.norton.modified_at)
        
    def test_physical_condition_label(self):
        field_label = self.norton._meta.get_field("physical_condition").verbose_name
        self.assertEqual(field_label, "physical condition")
    
    def test_mental_condition_label(self):
        field_label = self.norton._meta.get_field("mental_condition").verbose_name
        self.assertEqual(field_label, "mental condition")
        
    def test_activity_label(self):
        field_label = self.norton._meta.get_field("activity").verbose_name
        self.assertEqual(field_label, "activity")
        
    def test_mobility_label(self):
        field_label = self.norton._meta.get_field("mobility").verbose_name
        self.assertEqual(field_label, "mobility")
        
    def test_incontinence_label(self):
        field_label = self.norton._meta.get_field("incontinence").verbose_name
        self.assertEqual(field_label, "incontinence")
        
    def test_calculate_total_points(self):
        self.assertEqual(self.norton.calculate_total_points(), 20)
        
    def test_calculate_ris(self):
        self.assertEqual(self.norton.calculate_risk(), "Low Risk")
        
    def test_save_method(self):
        norton = NortonScale(
            hospitalization=self.hospitalization,
            created_by=self.user,
            physical_condition="3",
            mental_condition="3",
            activity="3",
            mobility="3",
            incontinence="4",
        )
        norton.save()
        self.assertIsNotNone(norton.total_points)
        self.assertIsNotNone(norton.pressure_risk)
class NewsScaleModelTest(TestCase):
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
        #cls.news.save()
        
    def test_valid_news_scale(self):
        self.assertEqual(self.news.respiratory_rate, 20)
        self.assertEqual(self.news.oxygen_saturation, 99)
        self.assertEqual(self.news.is_on_oxygen, False)
        self.assertEqual(self.news.aecopd_state, False)
        self.assertEqual(self.news.temperature, 36.6)
        self.assertEqual(self.news.systolic_blood_pressure, 120)
        self.assertEqual(self.news.diastolic_blood_pressure, 70)
        self.assertEqual(self.news.heart_rate, 64)
        self.assertEqual(self.news.level_of_consciousness, "awake")
        self.assertEqual(self.news.created_by, self.user)
        self.assertIsNotNone(self.news.created_at)
        self.assertIsNotNone(self.news.modified_at)
        self.assertLessEqual(self.news.created_at, self.news.modified_at)
        
    def test_respiratory_rate_label(self):
        field_label = self.news._meta.get_field("respiratory_rate").verbose_name
        self.assertEqual(field_label, "respiratory rate")
        
    def test_oxygen_saturation_label(self):
        field_label = self.news._meta.get_field("oxygen_saturation").verbose_name
        self.assertEqual(field_label, "oxygen saturation")
    
    def test_is_on_oxygen_label(self):
        field_label = self.news._meta.get_field("is_on_oxygen").verbose_name
        self.assertEqual(field_label, "is on oxygen")
        
    def test_aecopd_state_label(self):
        field_label = self.news._meta.get_field("aecopd_state").verbose_name
        self.assertEqual(field_label, "aecopd state")
        
    def test_temperature_label(self):
        field_label = self.news._meta.get_field("temperature").verbose_name
        self.assertEqual(field_label, "temperature")
        
    def test_systolic_blood_pressure_label(self):
        field_label = self.news._meta.get_field("systolic_blood_pressure").verbose_name
        self.assertEqual(field_label, "systolic blood pressure")
        
    def test_diastolic_blood_pressure_label(self):
        field_label = self.news._meta.get_field("diastolic_blood_pressure").verbose_name
        self.assertEqual(field_label, "diastolic blood pressure")
    
    def test_heart_rate_label(self):
        field_label = self.news._meta.get_field("heart_rate").verbose_name
        self.assertEqual(field_label, "heart rate")
    
    def test_level_of_consciousness_label(self):
        field_label = self.news._meta.get_field("level_of_consciousness").verbose_name
        self.assertEqual(field_label, "level of consciousness")
    
class PainScaleModelTest(TestCase):
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
        cls.pain = PainScale.objects.create(
            hospitalization=cls.hospitalization,
            created_by=cls.user,
            pain_level="5",
            pain_comment="",
        )
    
    def test_valid_pain_scale(self):
        self.assertEqual(self.pain.pain_level, "5")
        self.assertEqual(self.pain.pain_comment, "")
        self.assertEqual(self.pain.created_by, self.user)
        self.assertIsNotNone(self.pain.created_at)
        self.assertIsNotNone(self.pain.modified_at)
        self.assertLessEqual(self.pain.created_at, self.pain.modified_at)
        
    def test_pain_level_label(self):
        field_label = self.pain._meta.get_field("pain_level").verbose_name
        self.assertEqual(field_label, "pain level")
        
    def test_eye_response_label(self):
        field_label = self.pain._meta.get_field("pain_comment").verbose_name
        self.assertEqual(field_label, "pain comment")
    
    def test_calculate_pain_intepretation(self):
        self.assertEqual(self.pain.calculate_pain_intepretation(), "Moderate Pain")
        
    def test_save_method(self):
        pain = PainScale.objects.create(
            hospitalization=self.hospitalization,
            created_by=self.user,
            pain_level="10",
            pain_comment="Acute pain",
        )
        pain.save()
        self.assertIsNotNone(pain.pain_interpretation)

    def test_string_representation(self):
        # Test the __str__ representation
        expected_str = f"{self.pain.hospitalization.patient.first_name} - {self.pain.pain_level} - {self.pain.pain_interpretation}"
        self.assertEqual(str(self.pain), expected_str)