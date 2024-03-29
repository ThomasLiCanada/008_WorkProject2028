# Generated by Django 5.0 on 2024-01-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_keyword', models.CharField(max_length=255, null=True, unique=True)),
                ('supplier_inf', models.CharField(blank=True, max_length=255, null=True)),
                ('supplier_contact_person', models.CharField(blank=True, max_length=255, null=True)),
                ('supplier_contact_email', models.CharField(blank=True, max_length=255, null=True)),
                ('supplier_DHR_link', models.CharField(blank=True, max_length=1083, null=True)),
                ('supplier_ME', models.CharField(blank=True, max_length=255, null=True)),
                ('supplier_QE', models.CharField(blank=True, max_length=255, null=True)),
                ('supplier_Special_requirement', models.CharField(blank=True, max_length=1083, null=True)),
                ('supplier_File_Link', models.CharField(blank=True, max_length=1083, null=True)),
            ],
        ),
    ]
