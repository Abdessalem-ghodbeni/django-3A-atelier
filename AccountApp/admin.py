from django.contrib import admin

from AppointmentApp.admin import AppointmentInline
from .models import Doctor

# Register your models here.
from .models import Specialty
from .models import Patient
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name",)

    search_fields = ("name",)

    ordering = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "license_number",
        "phone",
    )

    list_filter = ("specialties",)

    search_fields = (
        "license_number",
        "last_name",
        "first_name",
    )

    ordering = ("last_name",)

    fieldsets = (
        (
            "Compte",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                )
            },
        ),
        (
            "Médecin",
            {
                "fields": (
                    "license_number",
                    "phone",
                    "specialties",
                )
            },
        ),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "national_id",
        "phone",
        "birth_date",
    )

    search_fields = (
        "last_name",
        "first_name",
        "national_id",
    )

    ordering = ("last_name",)

    fieldsets = (
        (
            "Compte",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                )
            },
        ),
        (
            "Patient",
            {
                "fields": (
                    "national_id",
                    "phone",
                    "birth_date",
                )
            },
        ),
    )
    inlines = [AppointmentInline]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                ),
            },
        ),
    )
