# Generated by Django 5.0.2 on 2024-04-18 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0014_semester_semester_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='semesters',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='courses',
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='Plan.semester'),
        ),
        migrations.AddField(
            model_name='semester',
            name='plan',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='Plan.plan'),
        ),
    ]