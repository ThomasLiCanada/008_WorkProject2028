# suppliers/models.py------------------------------------------------------------------------------
from django.db import models


class Supplier(models.Model):
    # supplier_name = models.CharField(max_length=255, null=True)
    supplier_keyword = models.CharField(max_length=255, null=True, unique=True)
    supplier_inf = models.CharField(max_length=255, null=True, blank=True)
    supplier_contact_person = models.CharField(max_length=255, null=True, blank=True)
    supplier_contact_email = models.CharField(max_length=255, null=True, blank=True)
    supplier_DHR_link = models.CharField(max_length=1083, null=True, blank=True)
    supplier_ME = models.CharField(max_length=255, null=True, blank=True)
    supplier_QE = models.CharField(max_length=255, null=True, blank=True)
    supplier_Special_requirement = models.CharField(max_length=1083, null=True, blank=True)
    supplier_File_Link = models.CharField(max_length=1083, null=True, blank=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def __str__(self):
        return self.supplier_keyword
