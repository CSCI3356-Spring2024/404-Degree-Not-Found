# Generated by Django 5.0.4 on 2024-05-07 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0025_plan_is_primary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='s1',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s2',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s3',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s4',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s5',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s6',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s7',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='plan',
            name='s8',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
