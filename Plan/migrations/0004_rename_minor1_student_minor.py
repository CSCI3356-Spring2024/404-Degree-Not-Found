# Generated by Django 5.0.2 on 2024-03-20 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0003_admin_advisor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='minor1',
            new_name='minor',
        ),
    ]
