from django.contrib import admin
from .models import ClinicServices, CategoryServices, Recipe


@admin.register(ClinicServices)
class ClinicServicesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(CategoryServices)
class CategoryServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)
    search_fields = ('title', 'price',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    list_filter = ('created',)
