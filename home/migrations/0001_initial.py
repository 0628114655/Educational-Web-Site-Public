# Generated by Django 5.1.3 on 2024-11-20 17:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('conclusion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('massar_num', models.CharField(blank=True, max_length=50, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('student_id', models.CharField(max_length=50)),
                ('sections', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='home.section')),
            ],
        ),
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='home.section')),
                ('students', models.ManyToManyField(related_name='classes', to='home.student')),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='subjects',
            field=models.ManyToManyField(related_name='sections', to='home.subject'),
        ),
        migrations.CreateModel(
            name='ExamMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_mark', models.FloatField(blank=True, null=True)),
                ('second_mark', models.FloatField(blank=True, null=True)),
                ('third_mark', models.FloatField(blank=True, null=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.section')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.subject')),
            ],
        ),
        migrations.CreateModel(
            name='ExamCorrection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', models.DateField(null=True)),
                ('margin1', models.TextField(blank=True, null=True)),
                ('margin2', models.TextField(blank=True, null=True)),
                ('margin3', models.TextField(blank=True, null=True)),
                ('margin4', models.TextField(blank=True, null=True)),
                ('margin5', models.TextField(blank=True, null=True)),
                ('section', models.ManyToManyField(to='home.section')),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.subject')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('section', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('content', models.TextField()),
                ('lastDate', models.DateField(null=True)),
                ('section', models.ManyToManyField(to='home.section')),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subject')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.userprofile')),
            ],
        ),
    ]
