from django.contrib import admin
from .models import *
import pandas as pd
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from django.templatetags.static import static

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'number_phone', 'sections', 'massar_num')
    search_fields = ['first_name', 'last_name']

class InsuranceNumberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('FirstName', 'LastName', 'MassarCode', 'Number')
    search_fields = ['FirstName', 'LastName', 'MassarCode', 'Number']

class StaffAdmin(ImportExportModelAdmin):
    list_display = ('FirstName', 'LastName', 'Email', 'PPR')
    search_fields = ['FirstName', 'LastName']

class AbsenceAdmin(ImportExportModelAdmin):
<<<<<<< HEAD
    list_display = ('student', 'status', 'absenceHours', 'section', 'dateTime', 'counter')
=======
    list_display = ('student', 'absenceHours', 'section', 'counter')
>>>>>>> a3a39f038fe874cf132da711fb9ddc76c29deb39
    search_fields = ['student', 'section']


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Insurance_number, InsuranceNumberAdmin)
admin.site.register(Section, )
admin.site.register(ExamMark,  )
admin.site.register(Announce)
admin.site.register(Home)
admin.site.register(Course)
admin.site.register(Image)
admin.site.register(HomeWork)
admin.site.register(UserProfile)
admin.site.register(Subject)
admin.site.register(ExamCorrection)
admin.site.register(Classe)
admin.site.register(Files)
admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Report)
admin.site.register(Activities)

