"""
URL configuration for StudentResultManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resultapp.views import edit_notice, index, admin_login, admin_dashboard, create_class, admin_logout, manage_class, edit_class, create_subject, manage_subject, edit_subject, create_subject_combination,manage_subject_combination, add_student, manage_student, edit_student, add_notice, manage_notice, add_result, get_student_subjects

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('admin-login/', admin_login, name='admin-login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create_class/', create_class, name='create_class'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    path('manage_class/', manage_class, name='manage_class'),
    path('edit_class/<int:class_id>/', edit_class, name='edit_class'),
    path('create_subject/', create_subject, name='create_subject'),
    path('manage_subject/', manage_subject, name='manage_subject'),
    path('edit_subject/<int:subject_id>/', edit_subject, name='edit_subject'),
    path('create_subject_combination/', create_subject_combination, name='create_subject_combination'),
    path('manage_subject_combination/', manage_subject_combination, name='manage_subject_combination'),
    path('add_student/', add_student, name='add_student'),
    path('manage_student/', manage_student, name='manage_student'),
    path('edit_student/<int:student_id>/', edit_student, name='edit_student'),
    path('add_notice/', add_notice, name='add_notice'),
    path('manage_notice/', manage_notice, name='manage_notice'),
    path('edit_notice/<int:notice_id>/', edit_notice, name='edit_notice'),
    path('add_result/', add_result, name='add_result'),
    path('get_student_subjects/', get_student_subjects, name='get_student_subjects'),
]
