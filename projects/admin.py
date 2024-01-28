from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.get_fields()]  # list all fields

    search_fields = ('supplier_name', 'product_description')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Project, ProjectAdmin)