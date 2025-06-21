from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns=[
    path('', views.home, name = 'home'),

    # تعرض فيها مختلف الأقسام
    path('classes/', views.classes, name = 'classes'),
    # تعرض فيها مجموع تلاميذ القسم
    path('ClassStudents/<int:id>', views.ClassStudents, name = 'ClassStudents'),
    # صفحة تعرض فيها البيانات الخاصة بانضباط التلميذ
    path('StudentAttendance/<int:id>', views.StudentAttendance, name = 'StudentAttendance'),

    # الصفحة الخاصة بتدبير غياب التلميذ
    path('studentAbsence/<int:id>', views.studentAbsence, name = 'studentAbsence'),
    # الصفحة الخاصة بتبيرالغياب الإجمالي للتلميذ
    path('studentTotalAbsence/<int:id>', views.studentTotalAbsence, name = 'studentTotalAbsence'),

    # صفحة خاصة بإضافة تقارير 
    path('add_reports/<int:id>', views.add_reports, name = 'add_reports'),
    path('studentTotalreports/<int:id>', views.studentTotalreports, name = 'studentTotalreports'),

    # االدالة الخاصة بإضافة الأنشطة
    path('add_activity/', views.add_activity, name = 'add_activity'),
    # الدالة الخاصة بعرض الأنشطة
    path('ShowActivities/', views.ShowActivities, name = 'ShowActivities'),

    # التأمين المدرسي
    path('add_insurance/', views.add_insurance, name = 'add_insurance'),
    path('insurance_list_export/', views.insurance_list_export, name = 'insurance_list_export'),

    path('offBudgetControl/', views.offBudgetControl, name = 'offBudgetControl'),


    path('Update/<int:id>/', views.Update, name = 'Update'),
    path('Delete/<int:id>/', views.Delete, name = 'Delete'),

    path('announce/', views.announce, name = 'announce'),
    path('add_announce/', views.add_announce, name = 'add_announce'),

    path('course_res/', views.course_res, name = 'course_res'),
    path('search/', views.search, name = 'search'),
    path('course/<int:id>', views.course, name = 'course'),
    path('add_course/', views.add_course, name = 'add_course'),
    path('UserCourseList/', views.UserCourseList, name = 'UserCourseList'),

    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('signout/', views.signout, name = 'signout'),

    path('UserHomeWorkList/', views.UserHomeWorkList, name = 'UserHomeWorkList'),
    path('HomeWorkView/<int:id>', views.HomeWorkView, name = 'HomeWorkView'),
    path('homeWork/', views.homeWork, name = 'homeWork'),

    path('UserInfo/', views.UserInfo, name = 'UserInfo'),

    path('exams/', views.exams, name = 'exams'),
    path('exam_marks/', views.exam_marks, name = 'exam_marks'),
    # الصفحات الخاصة بتصحيح الامتحان
    path('add_exam_correction/', views.add_exam_correction, name = 'add_exam_correction'),
    path('exam_research/', views.exam_research, name = 'exam_research'),
    path('exam_search_result/', views.exam_search_result, name = 'exam_search_result'),
    path('exam_correction/<int:id>', views.exam_correction, name = 'exam_correction'),
    # الصفحة الخاصة بتغيير كلمة المرور
    path('change-password/', PasswordChangeView.as_view(
        template_name='pages/password/change_password.html',
        success_url='/change-password/done/' 
    ), name='password_change'),
    path('change-password/done/', PasswordChangeDoneView.as_view(
        template_name='pages/password/password_change_done.html'
    ), name='password_change_done'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
