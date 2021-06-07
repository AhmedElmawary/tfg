from django.contrib import admin

from app import models
from coachapp import models as coach_models

# Register your models here.


class PackageAdmin(admin.ModelAdmin):
    autocomplete_fields=['user']
    list_display = (
        "id",
        "title",
        "description",
        "price",
        "yearly_price",
        "period",
        "currency",
        "start_date",
        "end_date",
    )


class CoachNotes(admin.TabularInline):
    model = coach_models.CoachNote


class UserAdmin(admin.ModelAdmin):
    search_fields = ['FirstName']

    list_display = (
        "id",
        "FirstName",
        "SecondName",
        "profile_pic",
        "email",
        "gender",
        "mobile",
        "is_staff",
    )
    readonly_fields = ("key",)
    inlines = [
        CoachNotes,
    ]


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "coach", "date", "direction", "from_gates")


class SessionAttendanceRequest(admin.ModelAdmin):
    list_display = ("id", "user", "coach", "session", "package", "date", "attended")


admin.site.register(models.User, UserAdmin)
# package category
admin.site.register(models.PackageCategory)
# package
admin.site.register(models.Package, PackageAdmin)
# sessions
admin.site.register(models.Session)
admin.site.register(models.SessionAttendanceRequest, SessionAttendanceRequest)
admin.site.register(models.SessionDates)
admin.site.register(models.SessionComments)


# session class
# admin.site.register(models.SessionClass)
# attendance
admin.site.register(models.Attendance, AttendanceAdmin)
admin.site.register(models.GeneralInfo)
admin.site.register(models.FAQ)
admin.site.register(models.Schedule)
admin.site.register(models.DifficultyLevel)
admin.site.register(models.SessionDay)
admin.site.register(models.SessionAt)
admin.site.register(models.SessionMonth)
