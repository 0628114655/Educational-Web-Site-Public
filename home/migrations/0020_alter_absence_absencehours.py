# Generated by Django 5.1.3 on 2025-04-14 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_hour_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='absenceHours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.hour'),
        ),
    ]
