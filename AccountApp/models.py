from django.db import models
from django.contrib.auth.models import AbstractUser
from AppointmentApp.admin import AppointmentInline

from django.core.exceptions import ValidationError
from django.utils import timezone

from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.
class User(AbstractUser):
    pass

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(
        max_length=6, unique=True, validators=[MinLengthValidator(6)]
    )

    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="Le téléphone doit contenir exactement 8 chiffres.",
            )
        ],
    )

    specialties = models.ManyToManyField(Specialty, related_name="doctors")

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}"


def validate_past_date(value):

    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$", message="Le CIN doit contenir exactement 8 chiffres."
            )
        ],
    )

    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="Le téléphone doit contenir exactement 8 chiffres.",
            )
        ],
    )

    birth_date = models.DateField(validators=[validate_past_date])

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
