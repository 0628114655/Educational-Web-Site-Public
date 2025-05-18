from django.shortcuts import render , HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone as time_zone 
from .decorator import allowed_user
from django.forms import modelformset_factory
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from collections import defaultdict
from django.core.mail import send_mail
from django.conf import settings
import urllib.parse
import calendar



ARABIC_MONTHS = [
    "", "يناير", "فبراير", "مارس", "أبريل", "ماي", "يونيو",
    "يوليوز", "غشت", "شتنبر", "أكتوبر", "نونبر", "دجنبر"
]

# الصفحة الرئيسية
def home (request): 
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info =  None
    context = {
        'user_info': user_info,
        'paragraphs' : Home.objects.all()
    }
    return render (request,'pages/home.html', context)

# الصفحة الخاصة بإضافة نشاط
@allowed_user(allowed_roles = ['admin', 'general_surveillance'])
def add_activity (request): 
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1) 
    form = Add_activity(request.POST or None)
    formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.none())
    if  request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            activity = form.save()
            for image_form in formset.cleaned_data:
                if image_form and image_form.get('image'):
                        Image.objects.create(
                            title = image_form.get('title'),
                            image = image_form.get('image'),
                            activity =activity
                        )
            
            messages.success (request, 'لقد تمت إضافة النشاط بنجاح.')
            return redirect('ShowActivities')

    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'ImageFormSet': formset,
        'form' : form,
        'user_info': user_info,
        'announces': Announce.objects.all()
        }
    return render (request,'pages/activities/add_activity.html', context)

# الصفحة الخاصة بعرض نشاط
def ShowActivities (request): 
    message = None
    activities = None    
    user = request.user

    if user.is_authenticated:   
        user_info = get_object_or_404(UserProfile, user=user)
    else:
        user_info = None 

    try:
        recent_activities = time_zone.now().date() - timedelta(days=15)
        activities = Activities.objects.filter(dateTime__gte=recent_activities)

        if not activities.exists():
            message = 'لا توجد أنشطة حاليا.'

    except Exception as e:
        print(f"Error: {e}")  
        message = 'حدث خطأ أثناء تحميل الإعلانات.'

    context = {
        'activities' : activities,
        'user_info': user_info,
        'message' : message
        }
    return render (request,'pages/activities/ShowActivities.html', context)

def announce (request):
    message = None
    announcements = None    
    user = request.user

    if user.is_authenticated:   
        user_info = get_object_or_404(UserProfile, user=user)
    else:
        user_info = None 

    try:
        recent_announces = time_zone.now().date() - timedelta(days=15)
        announcements = Announce.objects.filter(date__gte=recent_announces)

        if not announcements.exists():
            message = 'لا توجد إعلانات حاليا.'

    except Exception as e:
        print(f"Error: {e}")  
        message = 'حدث خطأ أثناء تحميل الإعلانات.'

    context = {
        'announces' : announcements,
        'user_info': user_info,
        'message' : message
        }
    return render (request,'pages/announce/announce.html', context)

# الدالة الخاصة بتحديث الإعلانات والدروس والواجبات الدراسية
@allowed_user(allowed_roles = ['admin', 'general_surveillance', 'teacher'])
def Update(request, id):
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    user_info = get_object_or_404(UserProfile, user=user)
    page = request.GET.get('page', '')
    editing_data = request.GET.get('editing_data', '')
    announce_form = None
    course_form = None
    homeWork_form = None
    activity_form = None
    CourseFormSet = None
    ActivityFormSet = None
    message = None
    imageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)
    FileFormSet = modelformset_factory(Files, form=FileForm, extra=1) 

    if request.method == 'GET':
        if page == 'announce':
            announce_form = get_object_or_404(Announce, id=id)         

        elif page == "course":
            course_form = get_object_or_404(Course, id=id)
            CourseFormSet = imageFormSet(queryset=Image.objects.none())
            
        elif page == 'homework':
            homeWork_form = HomeWork.objects.get(id = id)
            FileFormSet = FileFormSet(queryset=Files.objects.none())

        else:
            activity_form = get_object_or_404(Activities, id = id)  
            ActivityFormSet = imageFormSet(queryset=Image.objects.none())

    else:
        if editing_data == 'announce':
            title = request.POST.get('title')
            content = request.POST.get('content')
            announce = Announce.objects.get(id = id)
            if content and title:
                announce.title = title
                announce.content = content
                announce.save()
                messages.success(request, 'لقد تم تعديل الإعلان بنجاح.')   
                return redirect('announce')         
            
        elif editing_data == 'course':
            course = Course.objects.get(id = id)
            CourseFormSet = imageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
            title = request.POST.get("title")
            introduction = request.POST.get("introduction")
            subject = request.POST.get("subject")
            conclusion = request.POST.get("conclusion")
            if all ([title, introduction, subject, conclusion]):
                course.title = title
                course.introduction = introduction
                course.subject = subject
                course.conclusion = conclusion
                course.save()
                if CourseFormSet.is_valid():
                    for file_form in CourseFormSet:
                        title = file_form.cleaned_data.get('title')
                        image = file_form.cleaned_data.get('image')
                        Image.objects.create(
                            title = title,
                            image = image,
                            course = course
                        )

                messages.success(request, 'لقد تم تعديل الدرس بنجاح.')   
                return redirect ('UserCourseList')

        elif editing_data == 'homework':
            FileFormSet = FileFormSet(request.POST, request.FILES, queryset=Files.objects.none())
            title = request.POST.get("title")
            material = request.POST.get("material")
            material = Subject.objects.get(name = material)
            section_names = request.POST.getlist("section")
            sections = Section.objects.filter(name__in = section_names)
            content = request.POST.get("content")
            lastDate = request.POST.get("lastDate")
            homeWork = HomeWork.objects.get(id = id)
            print(homeWork.title)
            if all ([title and material and section_names and content and lastDate]):
                homeWork.title = title
                homeWork.material = material
                homeWork.section.set(sections)
                homeWork.content = content
                homeWork.lastDate = lastDate
                homeWork.user = user_profile
                homeWork.save()
                if FileFormSet.is_valid():
                    for file_form in FileFormSet:
                        title = file_form.cleaned_data.get('title')
                        file = file_form.cleaned_data.get('file')
                        Files.objects.create(
                            title = title,
                            file = file,
                            homework = HomeWork.objects.get(id = id)
                        )
                messages.success(request, 'لقد تم تعديل الواجب الدراسي بنجاح.')   
                return redirect ('UserHomeWorkList')
    
        elif editing_data == 'activity':
            activity = Activities.objects.get(id = id)
            ActivityFormSet = imageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
            try:
                title = request.POST.get("title")
                content = request.POST.get("content")
                dateTime = request.POST.get("dateTime")
                if all ([title, content, dateTime]):
                    activity.title = title
                    activity.content = content
                    activity.dateTime = dateTime
                    activity.save()
                    if ActivityFormSet.is_valid():
                        for file_form in ActivityFormSet:
                            title = file_form.cleaned_data.get('title')
                            image = file_form.cleaned_data.get('image')
                            Image.objects.create(
                                title = title,
                                image = image,
                                activity = activity
                            )

                    messages.success(request, 'لقد تم تعديل النشاط بنجاح.')   
                    return redirect ('ShowActivities')
    
            except Exception as e :
                message = 'لقد حدث خطأ غير متوقع المرجو إعادة المحاولة.'
                print(f'error is {e}')
    context = {
        'message' : message,
        'activity_form' : activity_form, 
        'activityFormSet' : ActivityFormSet,
        'FileFormSet': FileFormSet,
        'CourseFormSet': CourseFormSet,
        'all_sections' : Section.objects.all(),
        'all_materials' : Subject.objects.all(),
        'user_info' : user_info,
        'announce_form' :announce_form,
        'course_form' : course_form,
        'homeWork_form' : homeWork_form,
    }
    return render (request, 'pages/updateDelete/update.html', context)

# الدالة الخاصة بحذف الإعلانات والدروس والواجبات الدراسية
@allowed_user(allowed_roles = ['admin', 'general_surveillance', 'teacher'])
def Delete(request, id):
    page = request.GET.get('page', '')
    if page == 'announce':
        announce = get_object_or_404(Announce, id = id)
        announce.delete()
        messages.success(request, 'لقد تم حذف الإعلان بنجاح.')
        return redirect('announce')

    elif page == "course":
        course = get_object_or_404(Course, id = id)
        course.delete()
        messages.success(request, 'لقد تم حذف الدرس بنجاح.')
        return redirect ('UserCourseList')

    elif page == 'homework':
        homework = get_object_or_404(HomeWork, id = id)
        homework.delete()
        messages.success(request, 'لقد تم حذف الواجب المدرسي بنجاح.')
        return redirect ('UserHomeWorkList')
    
    elif page == 'activity':
        activity = get_object_or_404(Activities, id = id)
        activity.delete()
        messages.success(request, 'لقد تم حذف النشاط التربوي بنجاح.')
        return redirect ('ShowActivities')
    
    elif page == 'reports':
        report = get_object_or_404(Report, id = id)
        studentID = report.student.id
        report.delete()
        messages.success(request, 'لقد تم حذف التقرير بنجاح.') 
        referer = request.META.get('HTTP_REFERER')
        return redirect (referer, id = studentID )


    else:
        absence = get_object_or_404(Absence, id = id)
        studentID = absence.student.id
        absence.delete()
        messages.success(request, 'لقد تم حذف الغياب بنجاح.') 
        referer = request.META.get('HTTP_REFERER')
        return redirect (referer, id = studentID )

@allowed_user(allowed_roles = ["admin", 'general_surveillance', ])
def add_announce (request):
    form = Add_announce(request.POST or None)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        content = form.cleaned_data.get('content')
        data = Announce(
            title = title,
            content = content
        )
        data.save()
        return redirect('announce')

    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'form' : form,
        'user_info': user_info,
        'announces': Announce.objects.all()
        }
    return render (request,'pages/announce/add_announce.html', context)

# الدالة الخاصة بالبحث عن الدرس
def course_res (request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
    }
    return render (request,'pages/course/course_res.html', context)

# الدالة التي تظهر النتائج التي توافق البحث
def search(request):
    message = ''
    result = None
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            result = Course.objects.filter(subject__icontains = query)
            if not result.exists():
                message = 'لا توجد نتيجة تطابق نص البحث.'
    else:
        message = 'النص الذي تم إدخاله غير صالح، المرجو إدخال نص آخر!'
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'message' : message,
        'result' : result
    }
    return render(request, 'pages/course/search.html', context)

# الدالة التي تظهر النتيجة التي تم اختيارها 
def course(request, id):
    course = Course.objects.get(id = id)
    images = Image.objects.filter(course = id)
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'images' : images,
        'course' : course
    }
    return render(request, 'pages/course/course.html', context)

# الدالة التي تظهر الدروس التي أضافها المستخدم
@allowed_user(allowed_roles=['admin', 'general_surveillance', 'teacher'])
def UserCourseList(request):
    message = None
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    course = Course.objects.filter(user = user)
    if not course.exists():
        message = 'لا توجد دروس.'
    context = {
        'course': course,
        'user_info': user_info, 
        'message' : message
    }
    return render (request, 'pages/course/UserCourseList.html', context)

# الدالة الخاصة بإضافة الدروس
@allowed_user(allowed_roles=['admin', 'general_surveillance', 'teacher'])
def add_course(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1) 
    fileFormSet = modelformset_factory(Files, form=FileForm, extra=1) 
    if  request.method == 'POST':
        form = Add_course(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        fileFormSet = fileFormSet(request.POST, request.FILES, queryset=Files.objects.none())

        if form.is_valid() and formset.is_valid() and fileFormSet.is_valid():
            course = form.save()
            for image_form in formset.cleaned_data:
                    title = image_form.get('title')
                    image = image_form.get('image')
                    Image.objects.create(
                        title = title,
                        image = image,
                        course =course
                    )
            
            messages.success (request, 'لقد تمت إضافة الدرس بنجاح.')
            return redirect('UserCourseList')
    else:
        form = Add_course()
        formset = ImageFormSet(queryset=Image.objects.none())
        fileformset = fileFormSet(queryset=Files.objects.none())
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'formset': formset,
        'fileformset': fileformset,
        'form' : form,
        'user_info': user_info,
        'announces': Announce.objects.all()
        }
    return render (request,'pages/course/add_course.html', context)

# الدالة الخاصة بعرض الأقسام 
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def classes(request): 
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    classes = Section.objects.all()
    
    context = {
        'user_info' : user_info,
        'classes' : classes
    }
    return render(request, 'pages/attendance/classes.html', context)

# الدالة الخاصة بعرض التلاميذ حسب الأقسام
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def ClassStudents(request, id):
    message = None 
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    students = Student.objects.filter(sections = id)
    if not students:
        message = 'المرجو إضافة لائحة تلاميذ.'
    section = Section.objects.get(id = id)
    context = {
        'user_info' : user_info,
        'students' : students,
        'section' : section,
        'message' : message,
    }
    return render(request, 'pages/attendance/ClassStudents.html', context)

# الدالة الخاصة بعرض معلومات التلميذ المحدد
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def StudentAttendance(request, id):
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    student = Student.objects.get(id = id)
    
    context = {
        'user_info' : user_info,
        'student' : student
    }
    return render(request, 'pages/attendance/studentAttendance.html', context)

# الدالة الخاصة بعرض معلومات التلميذ المحدد
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def studentAbsence(request, id):
    whatsapp_url = None
    message = None
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    month = time_zone.now().date().month
    year = time_zone.now().date().year
    student = Student.objects.get(id = id)
    students = Student.objects.filter(sections = student.sections)
    monthlyAbsence = Absence.objects.filter(dateTime__month = month, dateTime__year = year,  student= student)
    monthlyAbsenceCount = Absence.objects.filter(dateTime__month = month, dateTime__year = year, student= student).count()
    session = Hour.objects.all()
  
    if request.method == 'POST':
        try:
            status = request.POST.get('status')
            notes = request.POST.get('notes', '/')
            date = request.POST.get('date')
            time = request.POST.get('time')
            hour = Hour.objects.get(id = time)
            send_message = (
                            f"ولي أمر التلميذ(ة) {student.first_name} {student.last_name}،\n"
                            f"نحيطكم علماً أنه تم تسجيل غياب ابنكم بتاريخ {date}.\n"
                            f"نوع الغياب: {status}\n"
                            f"ملاحظات إضافية: {notes}\n\n"
                            f"يرجى التواصل مع الإدارة لمزيد من التفاصيل.\n"
                        )
            Absence.objects.create(
                student = student,
                status = status,
                notes = notes,
                dateTime = date,
                absenceHours = hour,
                section = student.sections
            )
            number_phone = getattr(student , 'number_phone', None)
            if number_phone:
                try:

                    encoded_message = urllib.parse.quote(send_message)
                    whatsapp_url = f"https://wa.me/+212{number_phone}?text={encoded_message}"
                    # webbrowser.open(whatsapp_url)  

                except Exception as e:
                    print(f"فشل إرسال رسالة الواتساب: {e}")

            messages.success(request, 'لقد تمت إضافة غياب بنجاح.')
            # return redirect('studentAbsence', id = student.id)
            
        except Exception as e:
            message = 'لقد حدث خطأ غير متوقع'
            print('حدث خطأ غير متوقع:', e)
    context = {
        'message' : message,
        'session' : session,
        'user_info' : user_info,
        'student' : student,
        'students' : students,
        'monthlyAbsence' : monthlyAbsence,
        'monthlyAbsenceCount' : monthlyAbsenceCount,
        'whatsapp_url' : whatsapp_url,
    }
    return render(request, 'pages/attendance/absence/studentAbsence.html', context)
# الدالة الخاصة بعرض الغياب الإجمالي للتلميذ
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def studentTotalAbsence(request, id):
    whatsapp_url = None
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    student = Student.objects.get(id = id)
    absences_qs  = Absence.objects.filter(student = student).annotate(year = ExtractYear('dateTime'), month = ExtractMonth('dateTime')).order_by('-dateTime')
    grouped_absence = {}
    for absence in absences_qs :
        year = absence.year
        month = absence.month
        if year not in grouped_absence:
            grouped_absence[year] = {}
        if month not in grouped_absence[year]:
            grouped_absence[year][month] = []
        grouped_absence[year][month].append(absence)
    yearCount = {}  
    monthCount = {}
    for year, months in grouped_absence.items():
        totalAbsences = 0
        monthCount[year] = {}
        for month, absences in months.items():
            totalAbsences += len(absences_qs )
            monthCount[year][month] = len(absences)
        yearCount[year] = totalAbsences
    
    month = time_zone.now().month
    year = time_zone.now().year
    monthly_absences = absences_qs.filter(month=month, year=year)
    month_absences = monthly_absences.count()
    non_justify = monthly_absences.filter(status='غير مبرر').count()
    month = ARABIC_MONTHS[month]

    send_message = (
                            f"ولي أمر التلميذ(ة) {student.first_name} {student.last_name}،\n"
                            f"نحيطكم علماً أن مجموع غياب ابنكم خلال شهر  {month} من  هذا الموسم الدراسي بلغ {month_absences} (غياب) .\n"
                            f" منها {non_justify} (غياب) غير مبرر \n"
                           
                            f"يرجى التواصل مع الإدارة لمزيد من التفاصيل.\n"
                        )
    number_phone = getattr(student , 'number_phone', None)
    if number_phone:
        try:
            encoded_message = urllib.parse.quote(send_message)
            whatsapp_url = f"https://wa.me/+212{number_phone}?text={encoded_message}"
            # webbrowser.open(whatsapp_url)  

        except Exception as e:
            print(f"فشل إرسال رسالة الواتساب: {e}")

    context = {
        'whatsapp_url' : whatsapp_url,
        'yearCount' : yearCount,
        'monthCount' : monthCount,
        'user_info' : user_info,
        'student' : student,
        'grouped_absence' : dict(grouped_absence), 
        'month_absences' : month_absences
    }
    return render(request, 'pages/attendance/absence/studentTotalAbsence.html', context)

@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def ClassTotalAbsence(request, id):
    from collections import defaultdict
    user = request.user
    user_info = UserProfile.objects.get(user=user)
    section = Section.objects.get(id=id)
    students = Student.objects.filter(sections=section)

    grouped_absence = {}
    available_months = set()  # 🟡 لجمع (السنة، الشهر)

    for s in students:
        absences_qs = Absence.objects.filter(student=s).annotate(
            year=ExtractYear('dateTime'),
            month=ExtractMonth('dateTime'),
            day=ExtractDay('dateTime')
        ).order_by('-dateTime')

        if s not in grouped_absence:
            grouped_absence[s] = {}

        for absence in absences_qs:
            year = absence.year
            month = absence.month
            day = absence.day

            available_months.add((year, month))  # 🟡 تسجيل السنة والشهر

            if year not in grouped_absence[s]:
                grouped_absence[s][year] = {}
            if month not in grouped_absence[s][year]:
                grouped_absence[s][year][month] = {}
            grouped_absence[s][year][month][day] = 'X'

    # 🔵 حدد السنة والشهر الحاليين لعرضهم كبداية
    now = time_zone.now()
    year = now.year
    month = now.month

    days_in_month = calendar.monthrange(year, month)[1]
    days = list(range(1, days_in_month + 1))

    context = {
        'year': year,
        'month': month,
        'available_months': sorted(available_months, reverse=True),  # 🟢 لإرسال القائمة للواجهة
        'section': section,
        'user_info': user_info,
        'students': students,
        'grouped_absence': grouped_absence,
        'days': days
    }
    return render(request, 'pages/attendance/absence/ClassTotalAbsence.html', context)

# الدالة الخاصة بعرض وإضافة التقارير
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def add_reports(request, id):
    whatsapp_url = None
    message = None
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    student = Student.objects.get(id = id)
    all_materials = Subject.objects.all()
    material = None
    year = time_zone.now().year
    reports = Report.objects.filter(date__year = year, student = student)
    if request.method == 'POST':
        try:
            material_id =  request.POST.get('material')
            material = Subject.objects.get(id = material_id)
            report_content = request.POST.get('report_content')
            instructions = request.POST.get('instructions')
            date = request.POST.get('date')
            Report.objects.create(
                student = student,
                material = material,
                content = report_content,
                instructions = instructions,
                date = date,
            )
            messages.success(request, 'لقد تمت إضافة التقرير بنجاح.')
            send_message = (
                f"ولي أمر التلميذ(ة) {student.first_name} {student.last_name}،\n"
                f"نحيطكم علماً أنه تم تسجيل تقرير سلوكي بابنكم بتاريخ {date}.\n"
                f"تفاصيل التقرير:\n"
                f"الموضوع: {report_content}\n"
                f"ملاحظات إضافية: {instructions}\n\n"
                f"يرجى التواصل مع الإدارة لمزيد من التفاصيل.\n"
            )
            number_phone = getattr(student , 'number_phone', None)
            if number_phone:
                try:
                    encoded_message = urllib.parse.quote(send_message)
                    whatsapp_url = f"https://wa.me/+212{number_phone}?text={encoded_message}"
                    # webbrowser.open(whatsapp_url)  
                except Exception as e:
                    print(f"فشل إرسال رسالة الواتساب: {e}")
            # return redirect('add_reports', id = student.id)
        except Exception as e:
            message = 'لقد حدث خطأ غير متوقع'
            print(e)

    context = {
        'user_info' : user_info,
        'message' : message,
        'all_materials' : all_materials,
        'material' : material,
        'student': student,
        'reports' : reports,
        'whatsapp_url' : whatsapp_url
    }
    return render(request, 'pages/attendance/reports/add_reports.html', context)

# الدالة الخاصة بعرض سجل التقارير
@allowed_user(allowed_roles=['general_surveillance', 'admin'])
def studentTotalreports(request, id):
    whatsapp_url = None
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    student = Student.objects.get(id = id)
    reports_qs = Report.objects.filter(student = student).annotate(year = ExtractYear('date'), month = ExtractMonth('date')).order_by('-date')

    grouped_reports = {}
    for report in reports_qs:
        year = report.year
        month = report.month
        if year not in grouped_reports:
            grouped_reports[year] = {}
        if month not in grouped_reports[year]:
            grouped_reports[year][month] = []
        grouped_reports[year][month].append(report)
    yearCount = {}  
    monthCount = {}
    for year, months in grouped_reports.items():
        totalreports = 0
        monthCount[year] = {}
        for month, reports in months.items():
            totalreports += len(reports_qs)
            monthCount[year][month] = len(reports_qs)
        yearCount[year] = totalreports

    month = time_zone.now().month
    year = time_zone.now().year
    monthly_reports = reports_qs.filter(month=month, year=year)
    month_reports = monthly_reports.count()
    month = ARABIC_MONTHS[month]

    send_message = (
                            f"ولي أمر التلميذ(ة) {student.first_name} {student.last_name}،\n"
                            f"نحيطكم علماً أن مجموع التقارير السلوكية بابنكم خلال شهر  {month} من  هذا الموسم الدراسي بلغت {month_reports} (تقارير) .\n"
                            f"يرجى التواصل مع الإدارة لمزيد من التفاصيل.\n"
                        )
    number_phone = getattr(student , 'number_phone', None)
    if number_phone:
        try:
            encoded_message = urllib.parse.quote(send_message)
            whatsapp_url = f"https://wa.me/+212{number_phone}?text={encoded_message}"
            # webbrowser.open(whatsapp_url)  

        except Exception as e:
            print(f"فشل إرسال رسالة الواتساب: {e}")


    context = {
        'whatsapp_url' : whatsapp_url,
        'yearCount' : yearCount,
        'monthCount' : monthCount,
        'user_info' : user_info,
        'student' : student,
        'grouped_reports' : dict(grouped_reports), 
    }
    return render(request, 'pages/attendance/reports/studentTotalReports.html', context)

# الدالة التي تعرض الواجبات الدراسية الخاصة بالمستخدم
@allowed_user(allowed_roles=['admin', 'teacher'])
def UserHomeWorkList(request):
    message = None
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    homework = None
    try:
        homework = HomeWork.objects.filter(user = user_info)
 
        if not homework.exists():
            message = 'لم يتم وضع واجبات دراسية من قبل هذا المستخدم.'
    except Exception as e:
        print(f'The exception is {e}')
        message = 'حدث خطأ غير متوقع.'
    context = {
    'homework': homework,
    'user_info' : user_info,
    'message' : message
        }
    return render (request, 'pages/homework/UserHomeWorkList.html', context)

# الدالة التي تعرض الواجب الدراسي المختار من أجل تعديله أو حذفه
@allowed_user(allowed_roles=['teacher', 'admin'])
def HomeWorkView(request, id):
    user = request.user
    user_info = UserProfile.objects.get(user = user)
    message = None
    try:
        homeWork = HomeWork.objects.get(id = id)
    except Exception as e:
        message = 'حدث خطأ غير متوقع.'
    context = {
    'homeWork': homeWork,
    'user_info' : user_info,
    'message' : message
        }
    return render (request, 'pages/homework/HomeWorkView.html', context)

# الدالة التي تدبر وضعية الواجبات الدراسية سواء من حيث قراءة الواجبات من قبل التلاميذ أو إضافة الواجبات
@allowed_user(allowed_roles=['admin', 'teacher', 'student'])
def homeWork(request):
    templates_roles = {'student' : 'pages/homework/homeWork.html',
                        'admin' : 'pages/homework/add_homework.html',
                        'teacher' : 'pages/homework/add_homework.html'
                        }
    form = None
    user = request.user
    message = None
    user_info = None
    home_work = None
    user_group = user.groups.first()
    fileformset = None
    
    if user_group and user_group.name == 'student':
        try:
            now = time_zone.now().date()
            user_info = UserProfile.objects.get(user = user )
            student = Student.objects.get(massar_num = user)
            home_work = HomeWork.objects.filter(section__name = student.sections, lastDate__gte = now)
            if not home_work.exists():
                message = 'لا توجد أي واجبات دراسية.'
        except Exception as e:
            print(f"Unexpected error: {e}")
            user_info = UserProfile.objects.get(user = user)
            message = 'حدث خطأ غير متوقع.'
    else:
        user_info = UserProfile.objects.get(user = user)
        FileFormSet = modelformset_factory(Files, form=FileForm, extra=1) 

        if request.method == 'POST':
            form = Add_homework (request.POST)
            fileformset = FileFormSet(request.POST, request.FILES, queryset=Files.objects.none())
            if form.is_valid() and fileformset.is_valid():
                homework = form.save()
                if fileformset:
                    for image_form in fileformset.cleaned_data:
                        title = image_form.get('title')
                        file = image_form.get('file')
                        Files.objects.create(
                            title = title,
                            file = file,
                            homework = homework
                    )
                messages.success(request, 'لقد تمت إضافة الواجب الدراسي بنجاح.')
                return redirect('UserHomeWorkList')
        else:
            form = Add_homework()
            fileformset = FileFormSet(queryset=Files.objects.none())
    
    context = {
            'fileformset' : fileformset,
            'form' : form,
            'message' : message,
            'user_info': user_info,
            'home_work': home_work,
        }
    template = templates_roles.get(user_group.name, 'pages/homework/homeWork.html') 

    return render (request, template, context)

def signup(request):
    next = request.GET.get('next')
    form = UserRegistrationForm(request.POST, request.FILES or None)
    if request.user.is_authenticated:
        return HttpResponse ("You are not authorized to visit this page because you are already signed in.")
    else:
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user_type = form.cleaned_data.get('user_type')
            user.set_password(password)
            if user_type == 'student':
                student =  Student.objects.filter(first_name = firstname, last_name = lastname, massar_num = username).first()
                if student:
                    user.save()
                    student_group = Group.objects.get(name='student')  
                    user.groups.set([student_group])         
                    UserProfile.objects.create(
                        user = user,
                        firstname =firstname,
                        lastname = lastname,
                        User_Type = user_type,
                    )
                    messages.success(request, 'لقد تم تسجيل الاشتراك بنجاح.')
                    new_user = authenticate(username = username, password = password)
                    login(request, new_user) 
            else:
                staff =  Staff.objects.filter(FirstName = firstname, LastName = lastname, PPR = username).first()
                if staff:        
                    user.save() 
                    UserProfile.objects.create(
                        user = user,
                        firstname = firstname,
                        lastname = lastname,
                        email = email,
                        User_Type = user_type                
                        )
                    messages.success(request, 'لقد تم تسجيل الاشتراك بنجاح.')
                    new_user = authenticate(username = username, password = password)
                    login(request, new_user) 
            if next:
                return redirect(next)
            return redirect('/') 
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
        'form': form
    }   
    return render(request, 'pages/authentication/signup.html', context)

def signin(request):
    form = UserLoginForm(request.POST or None)
    if request.user.is_authenticated:
        return HttpResponse ("You are not authorized to visit this page because you are already signed in.")
    else:
        next = request.GET.get('next')
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password') 
            user = authenticate(username = username, password = password)
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('/')
    try:
            user = request.user
            user_info = UserProfile.objects.get(user = user)
    except:
            user_info = None
    context = {
            'user_info': user_info,
            'form': form
        }   
    return render(request, 'pages/authentication/signin.html', context)

def signout(request):
    logout (request)
    return redirect('/signin/')

@allowed_user(allowed_roles=['admin', 'teacher', 'general_survaillance', 'student'])
def UserInfo(request):
    user = request.user
    user_info = None
    staffInfo = None
    studentInfo = None
    message = None
    try:
        user_info = UserProfile.objects.get(user=user)
        try:
            staffInfo = Staff.objects.get(PPR=user.username)
        except Staff.DoesNotExist:
            pass

        try:
            studentInfo = Student.objects.get(massar_num=user.username)
        except Student.DoesNotExist:
            pass

    except Exception as e:
        message = 'لقد حدث خطأ غير متوقع'
        print(f'error id {e}')

    context = {
        'user_info': user_info,
        'staffInfo' : staffInfo,
        'studentInfo' : studentInfo,
        'message' : message,
    }
    return render (request, 'pages/userInfo.html', context)

# صفحة خاصة بعرض تصحيح الامتحان/نقط الامتحان
def exams(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
    }
    
    return render(request, 'pages/exams.html', context)

# الدالة الخاصة بإضافة تصحيح للامتحان
@allowed_user(allowed_roles=['admin', 'general_surveillance', 'teacher'])
def add_exam_correction(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
        form = Add_exam_correction(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('add_exam_correction')
    except:
        user_info = None
        form = None

    context = {
        'form': form,
        'user_info': user_info
    }
    return render(request, 'pages/exam correction/add_exam_correction.html', context)
# الدالة الخاصة بالبحث عن تصحيح الامتحان
def exam_research(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    context = {
        'user_info': user_info,
    }
    return render(request, 'pages/exam correction/exam_research.html', context)

# الدالة التي تظهر النتائج التي توافق البحث
def exam_search_result(request):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    result = None
    message = None
    exam_form = SearchForm(request.GET)
    if exam_form.is_valid():
        query = exam_form.cleaned_data.get('query')
        if query:
            result = ExamCorrection.objects.filter(content__contains = query)
            if not result.exists():
                    message = 'لا توجد نتيجة تطابق نص البحث.'
    else:
        message = 'النص الذي تم إدخاله غير صالح, المرجو إدخال نص آخر.'
    context = {
        'result' : result,
        'message' : message,
        'user_info': user_info,
    }
    return render(request, 'pages/exam correction/exam_research_result.html', context)

# الدالة التي تظهر النتيجة التي تم اختيارها 
def exam_correction(request, id):
    try:
        user = request.user
        user_info = UserProfile.objects.get(user = user)
    except:
        user_info = None
    result = ExamCorrection.objects.get(id = id )
    context = {
        'user_info': user_info,
        'result' : result
    }
    return render(request, 'pages/exam correction/exam_correction.html', context)

# صفحة مخصصة لعرض نقط الامتحان
def exam_marks(request):
    templates_roles = { 'student' : 'pages/exam_marks/exam_marks.html',
                        'admin' : 'pages/exam_marks/add_exam_marks.html',
                        'teacher' : 'templates/pages/exam_marks/add_exam_marks.html'
                    }
    user = request.user
    user_info = None
    mark = None
    message = None
    user_group = user.groups.first()
    if user_group and user_group == 'student':
        try:
            user_info = UserProfile.objects.get(user=user)
            mark = ExamMark.objects.filter(student__massar_num = user.username)
            if not mark.exists():
                message = 'لا توجد أية نقط امتحانات.'
            
        except UserProfile.DoesNotExist:
                message = 'المرجو تسجيل الدخول للاطلاع على نقط الامتحان.'

        except Exception as e:
                print(f"Unexpected error: {e}")
                message = 'حدث خطأ غير متوقع.'
    else:
        form = Add_exam_mark(request.POST or None)
        if form.is_valid():
            form.save()
            redirect('templates/pages/exam_marks/add_exam_marks.html')
    context = {
        'form' : form ,
        'user_info' : user_info,
        'mark' :  mark,
        'message': message,
    }
    template = templates_roles.get(user_group.name, 'templates/pages/exam_marks/exam_marks.html') 

    return render (request, template, context)


