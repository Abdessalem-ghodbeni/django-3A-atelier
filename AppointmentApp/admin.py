from django.contrib import admin


from .models import Appointment

from datetime import timedelta

from django.contrib import admin, messages
from django.utils import timezone

from .models import Appointment, Status


class AppointmentInline(admin.StackedInline):
    model = Appointment

    extra = 0

    show_change_link = True


class AppointmentDateFilter(admin.SimpleListFilter):
    title = "Date du rendez-vous"

    parameter_name = "date_rendez_vous"

    def lookups(self, request, model_admin):

        return [
            ("today", "Aujourd'hui"),
            ("week", "Cette semaine"),
            ("upcoming", "À venir"),
        ]

    def queryset(self, request, queryset):

        today = timezone.localdate()

        if self.value() == "today":
            return queryset.filter(appointment_date__date=today)

        if self.value() == "week":
            start_week = today - timedelta(days=today.weekday())

            end_week = start_week + timedelta(days=7)

            return queryset.filter(
                appointment_date__date__gte=start_week,
                appointment_date__date__lt=end_week,
            )

        if self.value() == "upcoming":
            return queryset.filter(appointment_date__gt=timezone.now())

        return queryset


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_date",
        "doctor",
        "patient",
        "duration_minutes",
        "status",
    )

    list_filter = (
        "status",
        "doctor",
        AppointmentDateFilter,
    )

    search_fields = (
        "patient__last_name",
        "patient__national_id",
        "doctor__last_name",
        "doctor__license_number",
    )

    ordering = ("-appointment_date",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Participants",
            {
                "fields": (
                    "doctor",
                    "patient",
                )
            },
        ),
        (
            "Planification",
            {
                "fields": (
                    "appointment_date",
                    "duration_minutes",
                    "status",
                )
            },
        ),
        (
            "Dossier",
            {
                "fields": (
                    "reason",
                    "prescription",
                )
            },
        ),
        (
            "Suivi",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.action(description="Confirmer les rendez-vous sélectionnés")
    def confirmer_rendez_vous(self, request, queryset):

        updated = queryset.update(status=Status.CONFIRMED)

        self.message_user(
            request, f"{updated} rendez-vous confirmés.", messages.SUCCESS
        )

    @admin.action(description="Annuler les rendez-vous sélectionnés")
    def annuler_rendez_vous(self, request, queryset):

        updated = queryset.update(status=Status.CANCELLED)

        self.message_user(request, f"{updated} rendez-vous annulés.", messages.SUCCESS)

    actions = [
        "confirmer_rendez_vous",
        "annuler_rendez_vous",
    ]
