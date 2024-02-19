from django.core.exceptions import ValidationError
from django.test import TestCase

from department.models import Department
from main.models import User


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
        department = Department.objects.create(
            name="Test Department", 
            description="This is a test department", 
            created_by=cls.user)
        
        cls.department_uuid = department.id
   
    def test_name_content(self):
        department = Department.objects.get(id=self.department_uuid)
        expected_object_name = f"{department.name}"
        self.assertEquals(expected_object_name, "Test Department")
        
    def test_name_label(self):
        department = Department.objects.get(id=self.department_uuid)
        field_label = department._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")
        
    def test_description_content(self):
        department = Department.objects.get(id=self.department_uuid)
        expected_object_name = f"{department.description}"
        self.assertEquals(expected_object_name, "This is a test department")
        
        # Test empty description
        department = Department.objects.create(name="Test", description="", created_by=self.user)
        expected_object_name = f"{department.description}"
        self.assertEquals(expected_object_name, "")
        
    def test_description_label(self):
        department = Department.objects.get(id=self.department_uuid)
        field_label = department._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")
        
    def test_field_validation(self):
        # Test validation rules for fields
        with self.assertRaises(ValidationError) as context:
            department = Department.objects.create(
                name="",
                description="Description",
                created_by=self.user
            )
            department.full_clean()
        self.assertIn('name', context.exception.message_dict)
        self.assertEqual(
        context.exception.message_dict['name'][0],
        'This field cannot be blank.'
    )
            
    def test_string_representation(self):
        # Test the __str__ representation
        department = Department.objects.get(id=self.department_uuid)
        self.assertEqual(str(department), "Test Department")
        
