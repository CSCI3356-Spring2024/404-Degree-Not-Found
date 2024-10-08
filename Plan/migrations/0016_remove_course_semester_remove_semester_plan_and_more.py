# Generated by Django 5.0.2 on 2024-04-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0015_remove_plan_semesters_remove_semester_courses_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='plan',
        ),
        migrations.AddField(
            model_name='plan',
            name='semesters',
            field=models.ManyToManyField(to='Plan.semester'),
        ),
        migrations.AddField(
            model_name='semester',
            name='courses',
            field=models.ManyToManyField(to='Plan.course'),
        ),
    ]
