# Generated by Django 5.1.3 on 2025-05-15 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0050_alter_files_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, default='صورة', max_length=100, null=True),
        ),
    ]
