from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    notices = Notice.objects.all().order_by('-posting_date')

    return render(
        request,
        'index.html',
        {
            'notices': notices
        }
    )

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
    subjects = Subject.objects.all()

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

    return render(request, 'manage_class.html', {
        'classes': classes,
        'subjects': subjects,
    })

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

        title = request.POST.get('title', '').strip()
        detail = request.POST.get('detail', '').strip()
        deadline = request.POST.get('deadline', '').strip()

        if not title or not detail or not deadline:

            messages.error(
                request,
                'Please fill in all required fields.'
            )

            return render(
                request,
                'add_notice.html'
            )

        try:

            Notice.objects.create(
                title=title,
                detail=detail,
                deadline=deadline
            )

            messages.success(
                request,
                'Notice published successfully.'
            )

            return redirect('manage_notice')

        except Exception as e:

            messages.error(
                request,
                f'Unable to publish notice: {e}'
            )

            return render(
                request,
                'add_notice.html'
            )

    return render(
        request,
        'add_notice.html'
    )

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


@login_required
def add_result(request):
    classes = Class.objects.all()

    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            student_id = request.POST.get('student_id')

            marks = {
                key.split('_')[1]: value
                for key, value in request.POST.items()
                if key.startswith('marks_')
            }

            for subject_id, mark in marks.items():
                Result.objects.create(
                    student_id=student_id,
                    student_class_id=class_id,
                    subject_id=subject_id,
                    marks=mark
                )

            messages.success(request, 'Result added successfully')
            return redirect('add_result')

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('add_result')

    return render(request, 'add_result.html', {
        'classes': classes
    })

from django.http import JsonResponse
@login_required
def get_student_subjects(request):
    class_id = request.GET.get('class_id')

    if not class_id:
        return JsonResponse({
            'students': [],
            'subjects': []
        })

    students = list(
        Student.objects
        .filter(student_class_id=class_id)
        .values('id', 'name')
    )

    subject_combinations = (
        SubjectCombination.objects
        .filter(
            student_class_id=class_id,
            status=1
        )
        .select_related('subject')
    )

    subjects = [
        {
            'id': sc.subject.id,
            'name': sc.subject.subject_name
        }
        for sc in subject_combinations
    ]

    return JsonResponse({
        'students': students,
        'subjects': subjects
    })

@login_required
def manage_result(request):

    classes = Class.objects.all()

    selected_class = request.GET.get('class_id')

    students_results = []

    if selected_class:

        # Get students who actually have results
        student_ids = Result.objects.filter(
            student_class_id=selected_class
        ).values_list(
            'student_id',
            flat=True
        ).distinct()

        students = Student.objects.filter(
            id__in=student_ids
        ).order_by('name')

        for student in students:

            results = Result.objects.filter(
                student=student,
                student_class_id=selected_class
            ).select_related(
                'subject'
            ).order_by(
                'subject__subject_name'
            )

            students_results.append({
                'student': student,
                'results': results,
            })

    return render(request, 'manage_result.html', {
        'classes': classes,
        'students_results': students_results,
        'selected_class': selected_class,
    })

@login_required
def edit_result(request, result_id):

    result = get_object_or_404(Result, id=result_id)

    if request.method == 'POST':

        marks = request.POST.get('marks')

        if marks:
            result.marks = marks
            result.save()

            messages.success(
                request,
                'Result updated successfully.'
            )

            return redirect('manage_result')

    return render(request, 'edit_result.html', {
        'result': result
    })

@login_required
def delete_result(request, result_id):

    result = get_object_or_404(Result, id=result_id)

    result.delete()

    messages.success(
        request,
        'Result deleted successfully.'
    )

    return redirect('manage_result')

@login_required
def admin_dashboard(request):

    student_count = Student.objects.count()
    subject_count = Subject.objects.count()
    class_count = Class.objects.count()
    result_count = Result.objects.count()

    return render(request, 'admin_dashboard.html', {
        'student_count': student_count,
        'subject_count': subject_count,
        'class_count': class_count,
        'result_count': result_count,
    })

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate


@login_required
def change_password(request):

    if request.method == 'POST':

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check all fields
        if not current_password or not new_password or not confirm_password:

            messages.error(
                request,
                'All password fields are required.'
            )

            return redirect('change_password')

        # Check current password
        if not request.user.check_password(current_password):

            messages.error(
                request,
                'Current password is incorrect.'
            )

            return redirect('change_password')

        # Check new password confirmation
        if new_password != confirm_password:

            messages.error(
                request,
                'New passwords do not match.'
            )

            return redirect('change_password')

        # Check minimum length
        if len(new_password) < 8:

            messages.error(
                request,
                'New password must contain at least 8 characters.'
            )

            return redirect('change_password')

        # Don't allow same password
        if current_password == new_password:

            messages.error(
                request,
                'New password must be different from your current password.'
            )

            return redirect('change_password')

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep the user logged in
        update_session_auth_hash(request, request.user)

        messages.success(
            request,
            'Password changed successfully.'
        )

        return redirect('admin_dashboard')

    return render(
        request,
        'change_password.html'
    )


def search_result(request):

    classes = Class.objects.all()

    return render(
        request,
        'search_result.html',
        {
            'classes': classes
        }
    )


def check_result(request):

    # Only allow POST requests
    if request.method != 'POST':
        return redirect('search_result')


    # Get submitted values
    student_id = request.POST.get('rollid', '').strip()
    class_id = request.POST.get('class', '').strip()


    # VALIDATION 1: Empty fields

    if not student_id:

        messages.error(
            request,
            'Please enter your Student ID.'
        )

        return redirect('search_result')


    if not class_id:

        messages.error(
            request,
            'Please select a class.'
        )

        return redirect('search_result')


    # VALIDATION 2: Check class

    try:

        selected_class = Class.objects.get(
            id=class_id
        )

    except Class.DoesNotExist:

        messages.error(
            request,
            'The selected class does not exist.'
        )

        return redirect('search_result')


    # VALIDATION 3: Check student

    try:

        student = Student.objects.get(
            id=student_id,
            student_class_id=class_id
        )

    except Student.DoesNotExist:

        messages.error(
            request,
            'No student found with this Student ID in the selected class.'
        )

        return redirect('search_result')


    # GET STUDENT RESULTS

    results = Result.objects.filter(
        student=student,
        student_class=selected_class
    ).select_related(
        'subject',
        'student_class'
    ).order_by(
        'subject__subject_name'
    )


    # VALIDATION 4: Check results

    if not results.exists():

        messages.error(
            request,
            f'No results have been added for {student.name} yet.'
        )

        return redirect('search_result')

    # CALCULATE RESULTS

    total_marks = sum(
        result.marks
        for result in results
    )


    result_count = results.count()


    # Maximum possible marks
    max_total_marks = result_count * 100


    # Average
    average_marks = (
        total_marks / result_count
        if result_count > 0
        else 0
    )


    # Percentage
    percentage = (
        (total_marks / max_total_marks) * 100
        if max_total_marks > 0
        else 0
    )


    percentage = round(
        percentage,
        2
    )


    average_marks = round(
        average_marks,
        2
    )


    # CALCULATE GRADE

    if percentage >= 75:

        grade = 'A'

    elif percentage >= 65:

        grade = 'B'

    elif percentage >= 55:

        grade = 'C'

    elif percentage >= 40:

        grade = 'S'

    else:

        grade = 'F'


    # PASS / FAIL

    # Assuming 40 is the pass mark
    failed_subjects = results.filter(
        marks__lt=40
    ).count()


    if failed_subjects == 0:

        status = 'PASS'

    else:

        status = 'FAIL'


    # SEND DATA TO TEMPLATE

    context = {

        'student': student,
        'selected_class': selected_class,
        'results': results,
        'total_marks': total_marks,
        'result_count': result_count,
        'max_total_marks': max_total_marks,
        'average_marks': average_marks,
        'percentage': percentage,
        'grade': grade,
        'status': status,
        'failed_subjects': failed_subjects,
    }


    return render(
        request,
        'result_page.html',
        context
    )