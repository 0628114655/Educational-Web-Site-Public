# Generated by Django 5.0.7 on 2025-04-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_absence_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('hour', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
