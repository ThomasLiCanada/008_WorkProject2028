# Generated by Django 5.0 on 2024-01-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receiving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_description', models.CharField(max_length=255, null=True)),
                ('part_number_formal', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]