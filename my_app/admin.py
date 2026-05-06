from django.contrib import admin
from users.models import Profile
from .models import (
    BodyArea,
    PainType,
    Stretch,
    Injury,
    StretchMapping,
    SavedStretch,
    Routine,
    RoutineLabel,
    RoutineStretch,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "nickname",
        "sport",
        "profile_picture",

    )

    search_fields = ("user__username", "nickname", "sport")

@admin.register(BodyArea)
class BodyAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_area")
    search_fields = ("name",)


@admin.register(PainType)
class PainTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Stretch)
class StretchAdmin(admin.ModelAdmin):
    list_display = ("name", "stretch_type", "difficulty_level")
    search_fields = ("name", "stretch_type", "difficulty_level")
    list_filter = ("stretch_type", "difficulty_level")


@admin.register(Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ("user", "pain_type", "severity", "date_occurred", "created_at")
    search_fields = ("user__username", "body_area__name", "pain_type__name")
    list_filter = ( "pain_type", "severity", "date_occurred")


@admin.register(StretchMapping)
class StretchMappingAdmin(admin.ModelAdmin):
    list_display = ("body_area", "pain_type", "stretch")
    search_fields = ("body_area__name", "pain_type__name", "stretch__name")
    list_filter = ("body_area", "pain_type")


@admin.register(SavedStretch)
class SavedStretchAdmin(admin.ModelAdmin):
    list_display = ("user", "stretch", "saved_at")
    search_fields = ("user__username", "stretch__name")
    list_filter = ("saved_at",)


@admin.register(RoutineLabel)
class RoutineLabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class RoutineStretchInline(admin.TabularInline):
    model = RoutineStretch
    extra = 1
    ordering = ("order_number",)


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "created_at")
    search_fields = ("title", "description", "difficulty")
    list_filter = ("difficulty", "labels")
    filter_horizontal = ("labels",)
    inlines = [RoutineStretchInline]