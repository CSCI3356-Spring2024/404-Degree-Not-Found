# Generated by Django 5.0.2 on 2024-04-28 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0024_plan_total_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
    ]
