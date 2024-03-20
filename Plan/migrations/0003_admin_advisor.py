# Generated by Django 5.0.3 on 2024-03-19 23:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan', '0002_user_delete_name_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Plan.user')),
            ],
            bases=('Plan.user',),
        ),
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Plan.user')),
            ],
            bases=('Plan.user',),
        ),
    ]