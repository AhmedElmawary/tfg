from django.contrib import admin

from app.models import User
from . import models



class CoachNoteAdmin(admin.ModelAdmin):
    model = models.CoachNote
    # fk_name = 'coach'

admin.site.register(models.CoachNote,CoachNoteAdmin)
