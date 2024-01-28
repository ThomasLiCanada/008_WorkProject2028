from django.contrib import admin
from .models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supplier._meta.get_fields()]  # list all fields

    search_fields = ('supplier_keyword',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Supplier, SupplierAdmin)
