from django.contrib import admin
from .models import ClinicPatients


@admin.register(ClinicPatients)
class ClinicPatientsAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'description', )
    search_fields = ('nickname', 'description', )