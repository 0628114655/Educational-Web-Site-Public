# Generated by Django 5.0.7 on 2025-05-22 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0053_alter_student_number_phone_alter_student_parentemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='number_phone',
            field=models.CharField(default=0, max_length=14),
        ),
        migrations.AlterField(
            model_name='student',
            name='parentEmail',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
