# Generated by Django 5.0 on 2024-01-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=255, null=True)),
                ('part_description', models.CharField(max_length=255, null=True)),
                ('project_inf', models.CharField(blank=True, max_length=255, null=True)),
                ('po_num', models.CharField(blank=True, max_length=128, null=True)),
                ('lot_num', models.CharField(blank=True, max_length=128, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, choices=[('STKTST', 'STKTST'), ('SHOTST', 'SHOTST'), ('STKNC', 'STKNC'), ('STKHOL', 'STKHOL'), ('STKPAC', 'STKPAC'), ('STKPRO', 'STKPRO'), ('STKINP', 'STKINP'), ('(see ACCPAC)', '(see ACCPAC)')], default='STKTST', max_length=128, null=True)),
                ('received_date', models.CharField(blank=True, max_length=128, null=True)),
                ('project_po_number_only', models.CharField(blank=True, max_length=255, null=True)),
                ('project_release_num', models.CharField(blank=True, max_length=128, null=True)),
                ('project_po_reversion', models.CharField(blank=True, max_length=128, null=True)),
                ('project_documentation_check_result', models.CharField(blank=True, max_length=2083, null=True)),
                ('project_documentation_check_result_ok', models.BooleanField(default=False)),
                ('project_parts_inspection_result', models.CharField(blank=True, max_length=2083, null=True)),
                ('project_parts_inspection_result_ok', models.BooleanField(default=False)),
                ('project_ncr_num', models.CharField(blank=True, max_length=128, null=True)),
                ('project_ncr_qty', models.IntegerField(blank=True, null=True)),
                ('project_label_checked', models.BooleanField(default=False)),
                ('project_dhr_reviewed', models.BooleanField(default=False)),
                ('project_parts_moved_pac_nc', models.BooleanField(default=False)),
                ('project_date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('project_label_checked_date', models.DateTimeField(blank=True, null=True)),
                ('project_dhr_reviewed_date', models.DateTimeField(blank=True, null=True)),
                ('project_parts_moved_pac_nc_date', models.DateTimeField(blank=True, null=True)),
                ('project_edhr', models.CharField(blank=True, max_length=2083, null=True)),
                ('project_inspector', models.CharField(blank=True, max_length=128, null=True)),
                ('project_final_accept_qty', models.IntegerField(blank=True, null=True)),
                ('ASANA', models.CharField(blank=True, max_length=2083, null=True)),
            ],
        ),
    ]