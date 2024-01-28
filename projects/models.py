# projects/models.py------------------------------------------------------------------------------
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Project(models.Model):
    supplier_name = models.CharField(max_length=255, null=True)
    part_description = models.CharField(max_length=255, null=True)
    project_inf = models.CharField(max_length=255, null=True, blank=True)
    # receiving excel file information into project's fields--------------------------------------
    po_num = models.CharField(max_length=128, null=True, blank=True)
    # supplier_name = models.CharField(max_length=128, null=True, blank=True)
    # part_description = models.CharField(max_length=255, null=True, blank=True)
    lot_num = models.CharField(max_length=128, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    LOCATION = (
        ('STKTST', 'STKTST'),
        ('SHOTST', 'SHOTST'),
        ('STKNC', 'STKNC'),
        ('STKHOL', 'STKHOL'),
        ('STKPAC', 'STKPAC'),
        ('STKPRO', 'STKPRO'),
        ('STKINP', 'STKINP'),
        ('(see ACCPAC)', '(see ACCPAC)'),
    )
    location = models.CharField(max_length=128, null=True, blank=True, choices=LOCATION, default='STKTST')
    received_date = models.CharField(max_length=128, null=True, blank=True)
    # project's items (itself fields)
    project_po_number_only = models.CharField(max_length=255, null=True, blank=True)
    project_release_num = models.CharField(max_length=128, null=True, blank=True)
    project_po_reversion = models.CharField(max_length=128, null=True, blank=True)
    project_documentation_check_result = models.CharField(max_length=2083, null=True, blank=True)
    project_documentation_check_result_ok = models.BooleanField(default=False)
    project_parts_inspection_result = models.CharField(max_length=2083, null=True, blank=True)
    project_parts_inspection_result_ok = models.BooleanField(default=False)
    project_ncr_num = models.CharField(max_length=128, null=True, blank=True)
    project_ncr_qty = models.IntegerField(null=True, blank=True)
    project_label_checked = models.BooleanField(default=False)
    project_dhr_reviewed = models.BooleanField(default=False)
    project_parts_moved_pac_nc = models.BooleanField(default=False)
    project_date_created = models.DateTimeField(auto_now_add=True, null=True)
    project_label_checked_date = models.DateTimeField(null=True, blank=True)
    project_dhr_reviewed_date = models.DateTimeField(null=True, blank=True)
    project_parts_moved_pac_nc_date = models.DateTimeField(null=True, blank=True)
    project_edhr = models.CharField(max_length=2083, null=True, blank=True)
    project_inspector = models.CharField(max_length=128, null=True, blank=True)
    project_file_local_path = models.CharField(max_length=2083, null=True, blank=True)
    # calculation fields
    project_final_accept_qty = models.IntegerField(null=True, blank=True)
    ASANA = models.CharField(max_length=2083, null=True, blank=True)

    def get_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def __str__(self):
        return self.supplier_name

    # Calculation: combine information to be ASANA and project_po_release_num etc.------------------------
    def generate_summary(self):

        # get po number only (i.e. number only)
        self.project_po_number_only = self.po_num[2:]

        # Combine information to be asana
        summary_text = ''

        # combine PO and release num to POxxxxxx-x
        self.project_po_release_num = f"{self.po_num} - {self.project_release_num}"

        # Calculate: final accept qty = lot qty - ncr qty
        if self.qty is not None and self.project_ncr_qty is not None:
            self.project_final_accept_qty = self.qty - self.project_ncr_qty
        if self.qty is not None and self.project_ncr_qty is None:
            # Calculate: final accept qty = lot qty - ncr qty
            self.project_final_accept_qty = self.qty
        return summary_text

    def save(self, *args, **kwargs):
        # Automatically update the summary field before saving
        self.ASANA = self.generate_summary()
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Project)
def update_checked_date(sender, instance, **kwargs):
    if instance.project_label_checked:
        pass
        if instance.project_label_checked_date:
            pass
        else:
            instance.project_label_checked_date = timezone.now()
    else:
        instance.project_label_checked_date = None


@receiver(pre_save, sender=Project)
def update_dhr_review_date(sender, instance, **kwargs):
    if instance.project_dhr_reviewed:
        if instance.project_dhr_reviewed_date:
            pass
        else:
            instance.project_dhr_reviewed_date = timezone.now()
    else:
        instance.project_dhr_reviewed_date = None


@receiver(pre_save, sender=Project)
def update_part_move_pac_nc_date(sender, instance, **kwargs):
    if instance.project_parts_moved_pac_nc:
        if instance.project_parts_moved_pac_nc_date:
            pass
        else:
            instance.project_parts_moved_pac_nc_date = timezone.now()
    else:
        instance.project_parts_moved_pac_nc_date = None


# if user input PO number without beginning with "PO", add "PO"
@receiver(pre_save, sender=Project)
def add_po_prefix(sender, instance, **kwargs):
    if instance.po_num and not instance.po_num.startswith('PO'):
        instance.po_num = f'PO{instance.po_num}'


# NCR num autofill "0" at the beginning
@receiver(pre_save, sender=Project)
def add_padding_to_ncr_num(sender, instance, **kwargs):
    if instance.project_ncr_num and len(instance.project_ncr_num) < 8:
        padding_length = 8 - len(instance.project_ncr_num)
        instance.project_ncr_num = '0' * padding_length + instance.project_ncr_num