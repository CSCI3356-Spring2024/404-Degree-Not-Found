# Generated by Django 5.0.3 on 2024-04-17 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0008_course_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='unique_semesters',
            field=models.BooleanField(default=False),
        ),
    ]
