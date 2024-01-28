# products/models.py------------------------------------------------------------------------------
from django.db import models


class Product(models.Model):
    part_number_formal = models.CharField(max_length=255, null=True, unique=True)
    part_inf = models.CharField(max_length=255, null=True, blank=True)
    part_number_no_dash = models.CharField(max_length=255, null=True, blank=True)
    part_name_official = models.CharField(max_length=255, null=True, blank=True)
    part_dmr = models.CharField(max_length=255, null=True, blank=True)
    part_gtin_number = models.CharField(max_length=255, null=True, blank=True)
    part_special_test = models.CharField(max_length=255, null=True, blank=True)
    part_ifu = models.CharField(max_length=255, null=True, blank=True)
    part_product_file = models.CharField(max_length=255, null=True, blank=True)
    part_edhr = models.CharField(max_length=255, null=True, blank=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def __str__(self):
        return self.part_number_formal
