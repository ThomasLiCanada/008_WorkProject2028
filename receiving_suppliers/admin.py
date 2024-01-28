from django.contrib import admin
from .models import ReceivingSupplier


class ReceivingSupplierAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReceivingSupplier._meta.get_fields()]  # list all fields

    search_fields = ('supplier_name', 'supplier_keyword')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(ReceivingSupplier, ReceivingSupplierAdmin)
