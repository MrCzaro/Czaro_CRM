import uuid
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import User

from department.models import (
    Consultation,
    Department,
    Hospitalization,
    Observation,
    VitalSigns,
)
from patient.models import Patient


class HospitalizationDetailViewTest(TestCase):
    @classmethod
    def setUp(cls):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse("department:hospitalization", args=[self.hospitalization.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.hospitalization.id}/hospitalization/",
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:hospitalization", args=[self.hospitalization.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hospitalization_detail.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:hospitalization", args=[self.hospitalization.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("bmis", response.context)
        self.assertIn("consultations", response.context)
        self.assertIn("glasgow_scales", response.context)
        self.assertIn("hospitalization", response.context)
        self.assertIn("observations", response.context)
        self.assertIn("news_scales", response.context)
        self.assertIn("norton_scales", response.context)
        self.assertIn("pain_scales", response.context)
        self.assertIn("vitals", response.context)
        self.assertIn("title", response.context)
        self.assertIn("back_url", response.context)

    def test_back_url(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:hospitalization", args=[self.hospitalization.id])
        )
        back_url = response.context["back_url"]
        self.assertEqual(back_url, reverse("patient:detail", args=[self.patient.id]))


class AdmitPatientViewTest(TestCase):
    @classmethod
    def setUp(cls):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse("department:admit_patient", args=[self.patient.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/login/?next=/department/{self.patient.id}/admit-patient/"
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:admit_patient", args=[self.patient.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admit_patient.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:admit_patient", args=[self.patient.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("departments", response.context)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("patient", response.context)

    def test_form_submission_valid_data(self):
        data = {
            "main_symptom": "Cough",
            "additional_symptoms": "Fever",
            "department_id": self.department.id,
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse("department:admit_patient", args=[self.patient.id]), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("department:department_detail", args=[self.department.id])
        )
        self.assertEqual(Hospitalization.objects.count(), 1)

    def test_form_submission_invalid_data(self):
        wrong_department_id = uuid.uuid4()
        data = {
            "main_symptom": "Cough",
            "additional_symptoms": "Fever",
            "department": wrong_department_id,
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse("department:admit_patient", args=[self.patient.id]), data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admit_patient.html")
        self.assertEqual(Hospitalization.objects.count(), 0)


class EditPatientSymptomsViewTest(TestCase):
    @classmethod
    def setUp(cls):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:hospitalization_update",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/hospitalization-edit/",
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:hospitalization_update",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_patient_admission.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:hospitalization_update",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("department_id", response.context)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("patient", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission(self):
        data = {
            "main_symptom": "Diarrhea",
            "additional_symptoms": "Nausea",
            "department_id": self.department.id,
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:hospitalization_update",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        updated_hospitalization = Hospitalization.objects.get(
            id=self.hospitalization.id
        )
        self.assertEqual(updated_hospitalization.main_symptom, "Diarrhea")
        self.assertEqual(updated_hospitalization.additional_symptoms, "Nausea")


class TransferPatientViewTest(TestCase):
    @classmethod
    def setUp(cls):
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
        cls.newdepartment = Department.objects.create(
            name="Test New Department",
            description="This is a test for a new department",
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:transfer", args=[self.patient.id, self.hospitalization.id]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/transfer/",
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:transfer", args=[self.patient.id, self.hospitalization.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transfer_patient.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:transfer", args=[self.patient.id, self.hospitalization.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("departments", response.context)
        self.assertIn("form", response.context)
        self.assertIn("hospitalization", response.context)
        self.assertIn("patient", response.context)
        self.assertIn("title", response.context)

    def test_form_submission(self):
        data = {
            "department": self.newdepartment.id,
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:transfer", args=[self.patient.id, self.hospitalization.id]
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:department_detail", args=[self.newdepartment.id]),
        )
        updated_hospitalization = Hospitalization.objects.get(
            id=self.hospitalization.id
        )
        self.assertEqual(updated_hospitalization.department, self.newdepartment)


class DischargePatientViewTest(TestCase):
    @classmethod
    def setUp(cls):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse("department:discharge", args=[self.hospitalization.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/login/?next=/department/{self.hospitalization.id}/discharge/"
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:discharge", args=[self.hospitalization.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "discharge_patient.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:discharge", args=[self.hospitalization.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("default_discharge_date", response.context)
        self.assertIn("default_discharge_time", response.context)
        self.assertIn("form", response.context)
        self.assertIn("hospitalization", response.context)
        self.assertIn("title", response.context)

    def test_form_submission(self):
        data = {
            "discharge_date": timezone.now().strftime("%Y-%m-%d"),
            "discharge_time": timezone.now().strftime("%H:%M"),
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse("department:discharge", args=[self.hospitalization.id]), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "department:department_detail",
                args=[self.hospitalization.department.id],
            ),
        )
        updated_hospitalization = Hospitalization.objects.get(
            id=self.hospitalization.id
        )
        self.assertEqual(updated_hospitalization.is_discharged, True)


class DepartmentDetailViewTest(TestCase):
    @classmethod
    def setUp(cls):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse("department:department_detail", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/login/?next=/department/{self.department.id}/"
        )

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:department_detail", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "department_detail.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:department_detail", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("department", response.context)
        self.assertIn("hospitalizations", response.context)
        self.assertIn("num_admitted_patients", response.context)
        self.assertIn("title", response.context)


class CreateDepartmentViewTest(TestCase):
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

    def test_authentication_required(self):
        response = self.client.get(reverse("department:create_department"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/department/create/")

    def access_denied_for_non_admins_professions(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(reverse("department:create_department"))
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:create_department"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "department_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:create_department"))
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("url", response.context)

    def test_form_submission_valid_data(self):
        data = {
            "name": "Test Department",
            "description": "Test Description Department",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:create_department"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:department_list"))
        self.assertEqual(Department.objects.count(), 1)

    def test_form_submission_invalid_data(self):
        data = {
            "name": "",
            "description": "Test Description Department",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(reverse("department:create_department"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "department_form.html")
        self.assertEqual(Department.objects.count(), 0)


class UpdateDepartmentViewTest(TestCase):
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
            created_by=cls.user,
        )

    def test_authentication_required(self):
        response = self.client.get(
            reverse("department:update_department", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/login/?next=/department/{self.department.id}/edit/"
        )

    def access_denied_for_non_admins_professions(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse("department:update_department", args=[self.department.id])
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:update_department", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "department_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:update_department", args=[self.department.id])
        )
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("url", response.context)

    def test_form_submission(self):
        data = {
            "name": "Test Department Edited",
            "description": "Test Description Department Edited",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse("department:update_department", args=[self.department.id]),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("department:department_detail", args=[self.department.id])
        )
        updated_department = Department.objects.get(id=self.department.id)
        self.assertEqual(updated_department.name, "Test Department Edited")
        self.assertEqual(
            updated_department.description, "Test Description Department Edited"
        )


class DeleteDepartmentViewTest(TestCase):
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
            created_by=cls.user,
        )

    def test_authentication_required(self):
        response = self.client.get(
            reverse("department:delete_department", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/login/?next=/department/{self.department.id}/delete/"
        )

    def access_denied_for_non_admins_professions(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse("department:delete_department", args=[self.department.id])
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:delete_department", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confirm_delete.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse("department:delete_department", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context)
        self.assertIn("name", response.context)
        self.assertIn("url", response.context)

    def test_department_deletion(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse("department:delete_department", args=[self.department.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("department:department_list"))
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(id=self.department.id)


class DepartmentListViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(
            first_name="AdminTest",
            last_name="User",
            email="testadmin@admin.com",
            password="adminpassword",
            profession="admins",
        )
        cls.first_department = Department.objects.create(
            name="The first Test Department",
            description="This is the first test department",
            created_by=cls.user,
        )
        cls.second_department = Department.objects.create(
            name="The second Test New Department",
            description="This is the second test department",
            created_by=cls.user,
        )
        cls.third_department = Department.objects.create(
            name="The third Test New Department",
            description="This is the third test department",
            created_by=cls.user,
        )
        cls.first_patient = Patient.objects.create(
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
        cls.second_patient = Patient.objects.create(
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
            patient=cls.first_patient,
            department=cls.first_department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )
        cls.hospitalization = Hospitalization.objects.create(
            patient=cls.second_patient,
            department=cls.second_department,
            main_symptom="Cough",
            additional_symptoms="Fever",
        )

    def test_authentication_required(self):
        response = self.client.get(reverse("department:department_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/department/list/")

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(reverse("department:department_list"))
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:department_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "department_list.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(reverse("department:department_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["department_counts"]), 3)
        self.assertEqual(response.context["total_admitted_patients"], 2)
        self.assertIn("departments", response.context)
        self.assertIn("department_counts", response.context)
        self.assertIn("title", response.context)
        self.assertIn("total_admitted_patients", response.context)


class CreatePatientConsultationViewTest(TestCase):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:consultation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-consultation-add/",
        )

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse(
                "department:consultation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:consultation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_consultation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:consultation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission_valid_data(self):
        data = {
            "consultation_name": "Test Consultation",
            "consultation": "This is content for a test.",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:consultation_create",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        self.assertEqual(Consultation.objects.count(), 1)

    def test_form_submission_invalid_data(self):
        data = {
            "consultation_name": "",
            # "consultation" : "This is content for a test."
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:consultation_create",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
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
        cls.consultation = Consultation.objects.create(
            hospitalization=cls.hospitalization,
            consultation_name="Test Consultation",
            consultation="This is content for a test.",
            created_by=cls.user,
        )

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:consultation_update",
                args=[self.patient.id, self.hospitalization.id, self.consultation.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-consultation-edit/{self.consultation.id}/",
        )

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse(
                "department:consultation_update",
                args=[self.patient.id, self.hospitalization.id, self.consultation.id],
            )
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:consultation_update",
                args=[self.patient.id, self.hospitalization.id, self.consultation.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_consultation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:consultation_update",
                args=[self.patient.id, self.hospitalization.id, self.consultation.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission(self):
        data = {
            "consultation_name": "Test Consultation Updated",
            "consultation": "This is content for a test - Updated.",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:consultation_update",
                args=[self.patient.id, self.hospitalization.id, self.consultation.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        updated_consultation = Consultation.objects.get(id=self.consultation.id)
        self.assertEqual(
            updated_consultation.consultation_name, "Test Consultation Updated"
        )
        self.assertEqual(
            updated_consultation.consultation, "This is content for a test - Updated."
        )


class CreatePatientObservationViewTest(TestCase):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:observation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-observation-add/",
        )

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse(
                "department:observation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:observation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_observation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:observation_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission_valid_data(self):
        data = {"observation": "This is content for a test."}
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:observation_create",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        self.assertEqual(Observation.objects.count(), 1)

    def test_form_submission_invalid_data(self):
        data = {}
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:observation_create",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
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
        cls.observation = Observation.objects.create(
            hospitalization=cls.hospitalization,
            observation="Observation 1",
            created_by=cls.user,
        )

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:observation_update",
                args=[self.patient.id, self.hospitalization.id, self.observation.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/patient-observation-edit/{self.observation.id}/",
        )

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse(
                "department:observation_update",
                args=[self.patient.id, self.hospitalization.id, self.observation.id],
            )
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:observation_update",
                args=[self.patient.id, self.hospitalization.id, self.observation.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patient_observation_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:observation_update",
                args=[self.patient.id, self.hospitalization.id, self.observation.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission(self):
        data = {
            "observation": "Updated observation.",
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:observation_update",
                args=[self.patient.id, self.hospitalization.id, self.observation.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        updated_observation = Observation.objects.get(id=self.observation.id)
        self.assertEqual(updated_observation.observation, "Updated observation.")


class CreateVitalSignsViewTest(TestCase):
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

    def test_authentication_required(self):
        response = self.client.get(
            reverse(
                "department:vitals_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/vital-signs-add/",
        )

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse(
                "department:vitals_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:vitals_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:vitals_create",
                args=[self.patient.id, self.hospitalization.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission_valid_data(self):
        data = {
            "respiratory_rate": 20,
            "oxygen_saturation": 99,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 70,
            "heart_rate": 64,
        }

        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:vitals_create",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        self.assertEqual(VitalSigns.objects.count(), 1)

    def test_form_submission_invalid_data(self):
        data = {
            "respiratory_rate": -20,
            "oxygen_saturation": 99,
            "temperature": 36.6,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 70,
            # "heart_rate" : 64,
        }

        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:vitals_create",
                args=[self.patient.id, self.hospitalization.id],
            ),
            data=data,
        )
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
        response = self.client.get(
            reverse(
                "department:vitals_update",
                args=[self.patient.id, self.hospitalization.id, self.vital.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/login/?next=/department/{self.patient.id}/{self.hospitalization.id}/vital-signs-edit/{self.vital.id}/",
        )

    def access_denied_for_secretaries(self):
        self.client.login(
            username="testsecretary@admin.com", password="secretarypassword"
        )
        response = self.client.get(
            reverse(
                "department:vitals_update",
                args=[self.patient.id, self.hospitalization.id, self.vital.id],
            )
        )
        self.assertRedirects(response, reverse("access_denied"))
        self.assertTemplateUsed(response, "access_denied.html")

    def test_successful_rendering(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:vitals_update",
                args=[self.patient.id, self.hospitalization.id, self.vital.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scale_form.html")

    def test_context_data(self):
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.get(
            reverse(
                "department:vitals_update",
                args=[self.patient.id, self.hospitalization.id, self.vital.id],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("title", response.context)
        self.assertIn("hospitalization_id", response.context)

    def test_form_submission(self):
        data = {
            "respiratory_rate": 18,
            "oxygen_saturation": 99,
            "temperature": 37.2,
            "systolic_blood_pressure": 120,
            "diastolic_blood_pressure": 70,
            "heart_rate": 64,
        }
        self.client.login(username="testadmin@admin.com", password="adminpassword")
        response = self.client.post(
            reverse(
                "department:vitals_update",
                args=[self.patient.id, self.hospitalization.id, self.vital.id],
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("department:hospitalization", args=[self.hospitalization.id]),
        )
        updated_vitals = VitalSigns.objects.get(id=self.vital.id)
        self.assertEqual(updated_vitals.respiratory_rate, 18)
        self.assertEqual(updated_vitals.oxygen_saturation, 99)
        self.assertEqual(updated_vitals.heart_rate, 64)
