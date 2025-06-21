from typing import Any
from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import *

User = get_user_model()
class SearchForm(forms.Form):
    query = forms.CharField(max_length=30)

class UserRegistrationForm(forms.ModelForm):
    USER_TYPE_CHOICES = (
        ('student', 'تلميذ'),
        ('staff', 'موظف'),
    )
    choices = [(choice, choice) for choice in ['','TCLSHF-1', 'TCLSHF-2', 'TCLSHF-3', 'TCLSHF-4','TCLSHF-5', 'TCLSHF-6', 'TCSF-1','TCSF-2', 'TCSF-3', 'TCSF-4', 'TCSF-5', '1BLSHF-1', '1BLSHF-2', '1BSEF-1', '1BSEF-2', '2BSHF-1', '2BSEF-2', '2BSVT-1', '2BSPF-1', '2BSPF-2' ]]
    password_confirmation = forms.CharField( label= 'تأكيد كلمة المرور*', widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    firstname = forms.CharField( label= ' الاسم الشخصي*' ,widget=forms.TextInput(attrs={'class': 'form-control',}))
    lastname = forms.CharField( label= 'الاسم العائلي*' ,widget=forms.TextInput(attrs={'class': 'form-control',}))
    email = forms.EmailField( label= 'البريد الإلكتروني*', widget=forms.EmailInput(attrs={'class': 'form-control', }))
    password = forms.CharField( label= 'كلمة المرور*', widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    user_type = forms.ChoiceField(label='الصفة*', choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    username = forms.CharField( label= 'رقم مسار/رقم التأجير*', widget=forms.TextInput(attrs={'class': 'form-control', }))
    class Meta:
        model = User
        fields = [ 'email','username','password']
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.order_fields([
            'firstname',
            'lastname',
            'username',
            'email',
            'user_type',
            'password',
            'password_confirmation',
        ])
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        user_type = self.cleaned_data.get('user_type')
        firstname = self.cleaned_data.get('firstname')
        lastname = self.cleaned_data.get('lastname')
        
        username_error = User.objects.filter(username = username)
        check_email =  User.objects.filter(email = email)

        if username_error.exists():
            raise forms.ValidationError('هذا الرمز موجود مسبقا.')
        if check_email.exists():
            raise forms.ValidationError ('هذا البريد الإلكتروني موجود مسبقا.')

        if password != password_confirmation:
            raise forms.ValidationError('كلمتا المرور لا تتطابقان!')
        
        if user_type == 'student':
            if not Student.objects.filter(first_name=firstname,  last_name = lastname , massar_num=username,).exists():
                raise forms.ValidationError('المعلومات لا تطابق أي تلميذ بالمؤسسة.')
        elif user_type == 'staff':
            if not Staff.objects.filter(FirstName=firstname, LastName = lastname,  PPR=username, ).exists():
                raise forms.ValidationError('المعلومات لا تطابق أي إطار بالمؤسسة.')

        return super(UserRegistrationForm, self).clean(*args, **kwargs)

class UserLoginForm(forms.Form):
    username = forms.CharField( label= 'رقم مسار/رقم التأجير', widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(label = 'كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user =  authenticate(password = password, username = username)
            if not user:
                raise forms.ValidationError(' رمز مسار/رقم التأجير أو كلمة المرور غير صحيحة.')
            return super(UserLoginForm, self).clean(*args, **kwargs)

class Add_announce(forms.ModelForm):
    title = forms.CharField( label= 'عنوان الإعلان' ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : ' عنوان الإعلان ..' }))
    content = forms.CharField( label= 'محتوى الإعلان' ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'اكتب محتوى الإعلان هنا ..'}),)
    class Meta:
        model = Announce
        fields = [ 'title', 'content']

class Add_course(forms.ModelForm):
    title = forms.CharField(label= ' عنوان الدرس', widget= forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'اكتب عنوان الدرس..'}))
    introduction = forms.CharField(label= ' مقدمة الدرس', widget= forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'اكتب مقدمة الدرس..'}),required=False)
    subject = forms.CharField(label= ' محتوى الدرس', widget= forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'اكتب محتوى الدرس..'}),required=False)
    conclusion = forms.CharField(label= ' خاتمة الدرس', widget= forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'اكتب خاتمة الدرس..'}),required=False)

    class Meta :
        model = Course
        fields = ['title', 'material', 'section' , 'introduction', 'subject', 'conclusion']

        labels = {
            'user' : 'المستخدم',
            'material': 'المادة',
            'section': 'القسم (لإضافة أكثر من قسم يرجى الضغط على ctrl ثم اختيار الأقسام)',
        }

        widgets = {
            'material': forms.Select(attrs={'class': 'form-control mb-3'}),
            'section': forms.SelectMultiple(attrs={'class': 'form-control mb-3'}),
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='الصورة', widget=forms.ClearableFileInput(attrs={'class': 'form-control'})) 
    title = forms.CharField(label='عنوان الصورة', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'أضف صورة..'}))
    class Meta:
        model = Image
        fields = ['title', 'image']

class Add_homework(forms.ModelForm):
    lastDate = forms.DateField(label='آخر أجل للتقديم', widget=forms.DateInput(attrs={'type' : 'date', 'class' : 'form-control'}))

    class Meta:
        model = HomeWork
        fields = ['user', 'title', 'content', 'lastDate', 'material', 'section']


        labels = {
                'user' : 'المستخدم',
                'title': 'عنوان  الواجب',
                'material': 'عنوان المادة',
                'content': 'محتوى الواجب الدراسي',
                'section': 'القسم',
        }
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان الواجب'}),
        'material': forms.Select(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'تفاصيل الواجب'}),
        'section': forms.SelectMultiple(attrs={'class': 'form-control'}),
    }
    def __init__(self, *args, **kwargs):
            super(Add_homework, self).__init__(*args, **kwargs)
            allowed_groups = ['admin', 'teacher', 'general_surveillance']
            self.fields['user'].queryset = UserProfile.objects.filter(user__groups__name__in=allowed_groups)
   
class FileForm(forms.ModelForm):
    title = forms.CharField(label='عنوان الملف', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'أضف عنوان الملف..'}))
    file = forms.FileField(required=False, label='الملف', widget=forms.ClearableFileInput(attrs={'class': 'form-control'})) 

    class Meta:
        model = Files
        fields = ['title', 'file']

class Add_exam_correction(forms.ModelForm):
    title = forms.CharField(label='العنوان' , widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder' : 'أضف العنوان'}))
    content = forms.CharField(label='التصحيح', widget=forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder' : 'أضف التصحيح'}))
    date = forms.DateField(label='تاريخ إجراء الامتحان', widget=forms.DateInput(attrs={'type' : 'date', 'class' : 'form-control'}))

    class Meta:
        model = ExamCorrection
        fields = ['title','material', 'section', 'content',  'date']

        labels = {
                'material': 'عنوان المادة',
                'section': 'القسم',
        }

        widgets = {
            'material': forms.Select(attrs={'class': 'form-control my-2'}),
            'section': forms.SelectMultiple(attrs={'class': 'form-control my-2'}),

        }

class Add_exam_mark(forms.ModelForm):
    first_mark = forms.DecimalField(label='نقطة الفرض الأول:', widget=forms.NumberInput(attrs = {'class' : 'form-control'}))
    second_mark = forms.DecimalField(label='نقطة الفرض الثاني:', widget=forms.NumberInput(attrs = {'class' : 'form-control'}))
    third_mark = forms.DecimalField(label='نقطة الفرض الثالث:', widget=forms.NumberInput(attrs = {'class' : 'form-control'}))
    class Meta:
        model =  ExamMark
        fields = ['student', 'first_mark', 'second_mark', 'third_mark', 'subject', 'section']

        labels = {
                    'subject': 'المادة',
                    'student': 'التلميذ',
                    'section': 'القسم',
            }

        widgets = {
        'student': forms.Select(attrs={'class': 'form-control'}),
        'subject': forms.Select(attrs={'class': 'form-control', }),
        'section': forms.SelectMultiple(attrs={'class': 'form-control'}),
                        }

class Add_activity(forms.ModelForm):
    title = forms.CharField(label='عنوان النشاط', widget=forms.TextInput(attrs={'class' : 'form-control',}))
    content = forms.CharField(label='محتوى النشاط', widget=forms.Textarea(attrs={'class' : 'form-control', }))
    dateTime = forms.DateTimeField(label='تاريخ إنجاز النشاط',    widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}))
    class Meta:
        model = Activities
        fields = ['title', 'dateTime', 'content']

class OffBudgetControl(forms.Form):
    Departures = forms.CharField(label='أسماء التلاميذ المغادرين: (الاسم الشخصي الاسم العائلي - الاسم الشخصي الاسم العائلي ...)', widget=forms.TextInput(attrs={'class' : 'form-control'}))
    ASS = forms.DecimalField(label='المبلغ المستخلص بالجمعية الرياضية', widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    HalfAmmount = forms.CharField(label='ضع أسماء التلاميذ الذين أدوا نصف مبلغ الجمعية الرياضية: (الاسم الشخصي الاسم العائلي - الاسم الشخصي الاسم العائلي ...)', widget=forms.TextInput(attrs={"class": "form-control"}))
    Insurance_fees = forms.DecimalField(label='مبلغ التأمين', widget=forms.NumberInput(attrs={"class": "form-control"}))