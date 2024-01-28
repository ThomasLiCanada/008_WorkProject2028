# supplier_products/models.py------------------------------------------------------------------------------
from django.db import models


class Supplier_Product(models.Model):
    supplier_keyword = models.CharField(max_length=255, null=True)
    part_number_formal = models.CharField(max_length=255, null=True)
    supplier_product_inf = models.CharField(max_length=255, null=True, blank=True)
    sps_part_reversion = models.CharField(max_length=255, null=True, blank=True)
    sps_ip_reversion = models.CharField(max_length=255, null=True, blank=True)
    supplier_product_ip_with_fields = models.CharField(max_length=1083, null=True, blank=True)
    sps_pn_supplier_edhr = models.CharField(max_length=255, null=True, blank=True)
    sps_special_requirement = models.CharField(max_length=255, null=True, blank=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def __str__(self):
        return self.supplier_keyword

