import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# =========================
# USER MANAGER
# =========================


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# =========================
# USER
# =========================


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def active_membership(self):
        return self.memberships.filter(is_active=True).order_by("-created_at").first()

    @property
    def active_organization(self):
        membership = self.active_membership()
        return membership.organization if membership else None

    def get_role(self, organization):
        membership = self.memberships.filter(
            organization=organization, is_active=True
        ).first()
        return membership.role if membership else None

    def __str__(self):
        return self.email


# =========================
# ORGANIZATION
# =========================


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_owner(self):
        membership = self.memberships.filter(role="owner", is_active=True).first()
        return membership.user if membership else None

    def __str__(self):
        return self.name


# =========================
# MEMBERSHIP
# =========================


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner"
        ADMIN = "admin"
        INSTRUCTOR = "instructor"
        STUDENT = "student"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )

    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"], name="unique_user_organization"
            )
        ]
        indexes = [
            models.Index(fields=["user", "organization"]),
            models.Index(fields=["organization", "role"]),
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.organization.name} ({self.role})"


# =========================
# BASE TENANT MODEL
# =========================


class BaseTenantModel(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="%(class)s_set"
    )

    class Meta:
        abstract = True
