from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as time_zone
from datetime import *


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    User_Type = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(null = True, blank=  True)    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Announce(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField(max_length = 500)
    date = models.DateField(default = time_zone.now)
    def __str__(self):
        return self.title
    
    @property
    def is_recent(self):
        return time_zone.now().date() - self.date <= timedelta(days = 15)
           
class Home(models.Model):
    title = models.CharField(max_length = 50)
    text = models.TextField()
    def __str__(self):
        return self.title
    
class Subject(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length = 50)
    subjects = models.ManyToManyField(Subject, related_name= 'sections' )
    def __str__(self):
        return self.name  

class Course(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, default=1 )
    material = models.ForeignKey(Subject, on_delete = models.CASCADE, default = 1)
    section = models.ManyToManyField(Section, default=1)
    title = models.CharField(max_length = 100, null = True, blank = True)
    introduction = models.TextField(null = True, blank = True)
    subject = models.TextField( null = True, blank = True)
    conclusion = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.title if self.title else 'درس بدون عنوان'

class Student(models.Model):
    massar_num = models.CharField(max_length = 50, null = True, blank = True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    sections = models.ForeignKey(Section, related_name="students", blank = True, null = True, on_delete = models.SET_NULL)
    number_phone = models.CharField(max_length = 14, default = 0000)
    parentEmail = models.EmailField(null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

class Staff(models.Model):
    choices =  [('أستاذ', 'أستاذ'), ('حارس عام', 'حارس عام'), ('مشرف', 'مشرف')]
    FirstName = models.CharField(max_length = 50)
    LastName = models.CharField(max_length = 50)
    PPR = models.CharField(max_length = 50)
    Mission = models.CharField(max_length = 100,choices =choices)
    Email = models.EmailField(null = True, blank = True)

    def __str__ (self):
        return f'{self.FirstName} {self.LastName}'

class Activities(models.Model):
    title = models.CharField(max_length=50)
    dateTime = models.DateField()
    content = models.TextField()

    @property
    def activity_images(self):
        images = self.image_set.all()
        return images

    def __str__(self):
        return f'نشاط حول موضوع: {self.title} بتاريخ {self.dateTime}'

class Image(models.Model):
    title = models.CharField(max_length = 100, default= 'صورة')
    course = models.ForeignKey(Course , on_delete = models.CASCADE, null = True, blank=True , default=None)
    activity = models.ForeignKey(Activities, on_delete= models.CASCADE, null = True, blank = True,  default=None)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        if self.course:
            return self.title if self.title else f"صورة لدرس {self.course.title}"
        else:
            return self.title if self.title else f"صورة لنشاط {self.activity.title}"

    @property
    def imgURL(self):
        if self.image.url:
            return self.image.url
        else:
            return ''
     
class HomeWork(models.Model):
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, blank = True)
    title = models.CharField(max_length = 100, null = True)
    material =  models.ForeignKey(Subject, on_delete = models.CASCADE, null = True)
    content = models.TextField()
    section =  models.ManyToManyField(Section)
    lastDate = models.DateField(null = True)

    def __str__(self):
        return self.title
    
    @property
    def remain(self):
        delta = self.lastDate - time_zone.now().date()
        return delta.days
    
    @property
    def is_two_days(self):
       return self.lastDate - time_zone.now().date() <= timedelta(days = 3)

class Files (models.Model):
    title = models.CharField(max_length = 100, default = 'ملف', null = True)
    homework = models.ForeignKey(HomeWork, on_delete = models.CASCADE, default=None , null=True, blank=True)
    file = models.FileField(null= True, blank= True)

    def __str__(self):
        if self.homework:
            return self.homework.title
        return "ملف بدون واجب"
    @property
    def fileURL(self):
        return self.file.url if self.file.url  else  ''
    
class ExamCorrection(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    material = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
    section = models.ManyToManyField(Section)
    date = models.DateField(null = True)

    def __str__(self):
        return self.title

class ExamMark(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    first_mark = models.FloatField(null=True, blank=True)
    second_mark = models.FloatField(null=True, blank=True)
    third_mark = models.FloatField(null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)  # إضافة حقل القسم
    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'
    
class Classe(models.Model):
    name = models.CharField(max_length=100, null = True)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL, related_name='classes')
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        if self.section:
            return f'Class: {self.name} in Section: {self.section.name}'
        else:
            return f'Class: {self.name} (No Section)'

class Report(models.Model):
    title = models.CharField(max_length=100, verbose_name="الإجراء الواجب اتخاذه")
    material = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="المادة")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="التلميذ")
    content = models.TextField(verbose_name="محتوى التقرير")
    instructions = models.TextField(verbose_name="الإجراء الواجب اتخاذه", default= '/')
    date = models.DateField(verbose_name="تاريخ التقرير")
    counter = models.PositiveIntegerField(null = True)
    def save(self, *args, **kwargs):
        if not self.counter:
            self.counter = Absence.objects.filter(student = self.student).count() + 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'تقرير عن التلميذ(ة): {self.student.first_name} {self.student.last_name}'

class Hour(models.Model):
    period_choice = [('الصباحية' , 'الصباحية'),('المسائية', 'المسائية')]
    title = models.CharField(max_length = 20)
    period = models.CharField( max_length = 20 , choices = period_choice)
    hour = models.TimeField()

    def __str__(self):
        return f' {self.title} من الفترة {self.period} '
    
class Absence(models.Model):
    status_choices = [('مبرر', 'مبرر'), ('غير مبرر', 'غير مبرر')]
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    notes = models.CharField(max_length=200)
    status = models.CharField(max_length=15, choices=status_choices)
    absenceHours = models.ForeignKey(Hour, on_delete=models.CASCADE)
    dateTime = models.DateField(null = True)
    counter = models.PositiveIntegerField()
    def save(self, *args, **kwargs):
        if not self.counter:
            self.counter = Absence.objects.filter(student = self.student).count() + 1
        super().save(*args, **kwargs)

    def __str__ (self):
        return f'غياب للتلميذ(ة) {self.student.first_name} {self.student.last_name} , بتاريخ {self.dateTime} ( {self.absenceHours} )'

    class Meta:
        ordering = ['-dateTime']

class Solution:
    def subsets(self, nums:list[int])-> list[list[int]]:
        n = len(nums)