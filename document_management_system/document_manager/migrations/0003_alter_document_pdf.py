# Generated by Django 3.2.6 on 2021-08-29 04:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0002_alter_document_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='PDF',
            field=models.FileField(upload_to='media', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
