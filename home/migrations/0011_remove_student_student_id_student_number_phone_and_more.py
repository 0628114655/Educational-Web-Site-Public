# Generated by Django 5.0.7 on 2025-04-07 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_image_image_alter_image_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student_id',
        ),
        migrations.AddField(
            model_name='student',
            name='number_phone',
            field=models.CharField(default=0, max_length=14),
        ),
        migrations.AlterField(
            model_name='files',
            name='title',
            field=models.CharField(default='ملف', max_length=100),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(default='صورة', max_length=100),
        ),
    ]
