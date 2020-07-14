from django.contrib import admin

from receipt.models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_price',)
    search_fields = ('name', 'full_price',)

