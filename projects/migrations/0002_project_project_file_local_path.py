# Generated by Django 5.0 on 2024-01-28 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_file_local_path',
            field=models.CharField(blank=True, max_length=2083, null=True),
        ),
    ]