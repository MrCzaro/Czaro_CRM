import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

USER_CHOICES = [
    ("nurses", "Nurse"),
    ("physicians", "Physician"),
    ("secretaries", "Secretary"),
    ("admins", "Admin"),
]


class CustomUserManager(UserManager):
    def _create_user_(
        self, first_name, last_name, email, password, profession, **extra_fields
    ):
        if not email:
            raise ValueError("Please type in an valid email address.")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            profession=profession,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        first_name=None,
        last_name=None,
        email=None,
        password=None,
        profession=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user_(
            first_name, last_name, email, password, profession, **extra_fields
        )

    def create_superuser(
        self,
        first_name=None,
        last_name=None,
        email=None,
        password=None,
        profession=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user_(
            first_name, last_name, email, password, profession, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=50, choices=USER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "profession",
    ]
