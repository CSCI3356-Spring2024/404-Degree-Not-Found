# Generated by Django 5.0.2 on 2024-04-27 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0023_alter_plan_s1_alter_plan_s2_alter_plan_s3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='total_credits',
            field=models.IntegerField(default=0),
        ),
    ]
