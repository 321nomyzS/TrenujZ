# Generated by Django 4.2.8 on 2025-03-23 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_tagcategory_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='short_description',
        ),
    ]
