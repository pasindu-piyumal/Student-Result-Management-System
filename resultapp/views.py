from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    return render(request, 'index.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid credentials or not authorized'
    return render(request, 'admin_login.html', locals())

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    return render(request, 'admin_dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@login_required
def create_class(request):
    if request.method == 'POST':
        try:
            class_name = request.POST.get('classname', '').strip().title()
            class_numeric = request.POST.get('classnamenumeric', '').strip()  
            section = request.POST.get('section', '').strip().title()
            Class.objects.create(class_name=class_name, class_numeric=class_numeric, section= section)
            messages.success(request, 'Class created successfully')
            return redirect('create_class')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('create_class')
    return render(request, 'create_class.html')

@login_required
def manage_class(request):
    classes = Class.objects.all()

    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_object = get_object_or_404(Class, id=class_id)
            class_object.delete()
            messages.success(request, 'Class deleted successfully')
            return redirect('manage_class')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_class')

    return render(request, 'manage_class.html', locals())


@login_required
def edit_class(request, class_id):
    class_object = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        class_name = request.POST.get('classname')
        class_numeric = request.POST.get('classnamenumeric')
        section = request.POST.get('section')
        try:
            class_object.class_name = class_name
            class_object.class_numeric = class_numeric
            class_object.section = section
            class_object.save()
            messages.success(request, 'Class edited successfully')
            return redirect('manage_class')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('edit_class')
    return render(request, 'edit_class.html', locals())

@login_required
def create_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectname').strip().title()
            subject_code = request.POST.get('subjectcode').strip().upper()
            Subject.objects.create(subject_name=subject_name, subject_code=subject_code)
            messages.success(request, 'Subject created successfully')
            return redirect('create_subject')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('create_subject')
    return render(request, 'create_subject.html')

@login_required
def manage_subject(request):
    subjects = Subject.objects.all()

    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            subject_object = get_object_or_404(Subject, id=subject_id)
            subject_object.delete()
            messages.success(request, 'Subject deleted successfully')
            return redirect('manage_subject')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_subject')

    return render(request, 'manage_subject.html', locals())

@login_required
def edit_subject(request, subject_id):
    subject_object = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject_name = request.POST.get('subjectname')
        subject_code = request.POST.get('subjectcode')

        try:
            subject_object.subject_name = subject_name
            subject_object.subject_code = subject_code
            subject_object.save()
            messages.success(request, 'Subject edited successfully')
            return redirect('manage_subject')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('edit_subject')
    return render(request, 'edit_subject.html', locals())

@login_required
def create_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            subject_id = request.POST.get('subject')
            SubjectCombination.objects.create(student_class_id=class_id, subject_id=subject_id, status=1)
            messages.success(request, 'Subject combination created successfully')
            return redirect('create_subject')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('create_subject_combination')
    return render(request, 'create_subject_combination.html', locals())

@login_required
def manage_subject_combination(request):
    combinations = SubjectCombination.objects.all()
    activate_id = request.GET.get('activate_id')
    deactivate_id = request.GET.get('deactivate_id')

    if request.GET.get('activate_id'):
        try:
            SubjectCombination.objects.filter(id = activate_id).update(status=1)
            messages.success(request, 'Subject Combiantion activated successfully')
            return redirect('manage_subject_combination')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_subject_combination')
        
    if request.GET.get('deactivate_id'):
        try:
            SubjectCombination.objects.filter(id = deactivate_id).update(status=0)
            messages.success(request, 'Subject Combiantion deactivated successfully')
            return redirect('manage_subject_combination')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_subject_combination')

    return render(request, 'manage_subject_combination.html', locals())


@login_required
def add_student(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            full_name = request.POST.get('fullname')
            student_id = request.POST.get('indexnumber')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            class_id = request.POST.get('class')
            student_class = Class.objects.get(id=class_id)
            Student.objects.create(name=full_name, id=student_id, email=email, gender=gender, dob=dob, student_class=student_class)
            messages.success(request, 'Student added successfully')
            return redirect('add_student')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('add_student')
    return render(request, 'add_student.html', locals())

@login_required
def manage_student(request):
    students = Student.objects.all()        
    if request.GET.get('delete'):
        try:
            student_id = request.GET.get('delete')
            student_object = get_object_or_404(Student, id=student_id)
            student_object.delete()
            messages.success(request, 'Student deleted successfully')
            return redirect('manage_student')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_student')

    return render(request, 'manage_student.html', locals())

@login_required
def edit_student(request, student_id):
    student_object = get_object_or_404(Student, id=student_id)
    classes = Class.objects.all()
    if request.method == 'POST':
        full_name = request.POST.get('name')
        std_id = request.POST.get('id')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        class_id = request.POST.get('class')
        status = request.POST.get('status')

        try:
            student_object.name = full_name
            student_object.id = std_id
            student_object.email = email
            student_object.gender = gender
            student_object.dob = dob
            student_object.student_class = Class.objects.get(id=class_id)
            student_object.status = status
            student_object.save()
            messages.success(request, 'Student edited successfully')
            return redirect('manage_student')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('edit_student', student_id=student_id)
    return render(request, 'edit_student.html', locals())

@login_required
def add_notice(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            Notice.objects.create(title=title, detail=detail)
            messages.success(request, 'Notice added successfully')
            return redirect('add_notice')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('add_notice')
    return render(request, 'add_notice.html', locals())

@login_required
def manage_notice(request):
    notices = Notice.objects.all()
    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_object = get_object_or_404(Notice, id=notice_id)
            notice_object.delete()
            messages.success(request, 'Notice deleted successfully')
            return redirect('manage_notice')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_notice')

    return render(request, 'manage_notice.html', locals())

@login_required
def edit_notice(request, notice_id):
    notice_object = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail')

        try:
            notice_object.title = title
            notice_object.detail = detail
            notice_object.save()
            messages.success(request, 'Notice edited successfully')
            return redirect('manage_notice')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('edit_notice', notice_id=notice_id)
    return render(request, 'edit_notice.html', locals())
