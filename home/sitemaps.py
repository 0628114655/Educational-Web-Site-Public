from django.contrib.sitemaps import Sitemap
from .models import (
    Announce, Home, Subject, Section, Course,
    Student, Staff, Activities, HomeWork,
    ExamCorrection,  Report, Absence
)
from django.utils.timezone import now


class AnnounceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Announce.objects.all()

    def lastmod(self, obj):
        return obj.date

class HomeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Home.objects.all()

class SubjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Subject.objects.all()

class SectionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Section.objects.all()

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Course.objects.all()

class StudentSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Student.objects.all()

class StaffSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Staff.objects.all()

class ActivitiesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Activities.objects.all()

    def lastmod(self, obj):
        return obj.dateTime

class HomeWorkSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return HomeWork.objects.all()

    def lastmod(self, obj):
        return obj.lastDate

class ExamCorrectionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return ExamCorrection.objects.all()

class ClasseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Classe.objects.all()

class ReportSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Report.objects.all()

    def lastmod(self, obj):
        return obj.date

class AbsenceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return Absence.objects.all()

    def lastmod(self, obj):
        return obj.dateTime
