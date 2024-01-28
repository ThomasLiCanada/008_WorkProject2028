# receiving_suppliers/models.py------------------------------------------------------------------------------
from django.db import models


class ReceivingSupplier(models.Model):
    supplier_name = models.CharField(max_length=255, null=True)
    supplier_keyword = models.CharField(max_length=255, null=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def __str__(self):
        return self.supplier_name
