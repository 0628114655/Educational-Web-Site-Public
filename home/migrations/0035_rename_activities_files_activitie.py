# Generated by Django 5.1.8 on 2025-05-03 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_alter_files_activities_alter_files_course_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='activities',
            new_name='activitie',
        ),
    ]
