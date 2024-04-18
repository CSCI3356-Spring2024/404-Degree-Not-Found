# Generated by Django 5.0.2 on 2024-04-18 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0017_remove_plan_semesters_remove_semester_courses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='Plan.semester'),
        ),
        migrations.AlterField(
            model_name='semester',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='Plan.plan'),
        ),
    ]
