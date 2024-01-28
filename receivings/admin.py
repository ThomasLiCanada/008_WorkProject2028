from django.contrib import admin
from .models import Receiving


class ReceivingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Receiving._meta.get_fields()]  # list all fields

    search_fields = ('part_number_formal', 'part_description')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Receiving, ReceivingAdmin)