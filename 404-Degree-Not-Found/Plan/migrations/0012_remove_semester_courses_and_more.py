# Generated by Django 5.0.2 on 2024-04-18 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0011_alter_plan_semester_1_alter_plan_semester_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='semester_number',
        ),
        migrations.AddField(
            model_name='semester',
            name='course_1_code',
            field=models.CharField(default='XXXX0000', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='course_2_code',
            field=models.CharField(default='XXXX0000', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='course_3_code',
            field=models.CharField(default='XXXX0000', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='course_4_code',
            field=models.CharField(default='XXXX0000', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='course_5_code',
            field=models.CharField(default='XXXX0000', max_length=50),
            preserve_default=False,
        ),
    ]
