# receivings/models.py------------------------------------------------------------------------------
from django.db import models


class Receiving(models.Model):
    part_description = models.CharField(max_length=255, null=True)
    part_number_formal = models.CharField(max_length=255, null=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def __str__(self):
        return self.part_description
