# Generated by Django 5.0.7 on 2025-05-03 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_alter_image_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='file',
        ),
    ]
