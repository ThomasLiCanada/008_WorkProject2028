from django.contrib import admin
from .models import Supplier_Product


class Supplier_ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supplier_Product._meta.get_fields()]  # list all fields

    search_fields = ('supplier_keyword', 'part_number_formal')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Supplier_Product, Supplier_ProductAdmin)