# Generated by Django 5.0.7 on 2025-04-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_report_instructions_alter_report_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='counter',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
