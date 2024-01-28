# Generated by Django 5.0 on 2024-01-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number_formal', models.CharField(max_length=255, null=True, unique=True)),
                ('part_inf', models.CharField(blank=True, max_length=255, null=True)),
                ('part_number_no_dash', models.CharField(blank=True, max_length=255, null=True)),
                ('part_name_official', models.CharField(blank=True, max_length=255, null=True)),
                ('part_dmr', models.CharField(blank=True, max_length=255, null=True)),
                ('part_gtin_number', models.CharField(blank=True, max_length=255, null=True)),
                ('part_special_test', models.CharField(blank=True, max_length=255, null=True)),
                ('part_ifu', models.CharField(blank=True, max_length=255, null=True)),
                ('part_product_file', models.CharField(blank=True, max_length=255, null=True)),
                ('part_edhr', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
