"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('contact/', views.contact),
    path('about/', views.about),
    path('admindashboard/', views.admindashboard),
    
    path('departmentaddedbyadmin/', views.add_department, name="adddepartmentbyadmin"),
    path('departmentupdatedbyadmin/', views.update_department, name="updatedepartmentbyadmin"),
    path('departmentdeletedbyadmin/', views.delete_department, name="deletedepartmentbyadmin"),

    path('doctoraddedbyadmin/', views.add_doctor, name="adddoctorbyadmin"),
    path('doctorupdatedbyadmin/', views.update_doctor, name="updatedoctorbyadmin"),
    path('doctordeletedbyadmin/', views.delete_doctor, name="deletedoctorbyadmin"),


    path('patientaddedbyadmin/', views.add_patient, name="addpatientbyadmin"),
    path('patientupdatedbyadmin/', views.update_patient, name="updatepatientbyadmin"),
    path('patientdeletedbyadmin/', views.delete_patient, name="deletepatientbyadmin"),
    
    path('appointmentremoved<int:pid><int:aid>/', views.remove_appointment, name="removeappointment"),
    path('doctorremoved<int:did><int:aid>/', views.remove_doctor, name="removedoctor"),
    path('patientdashboard/', views.patientdashboard),

    path('profileupdated/', views.update_profile, name="updateprofile"),
    path('appointmentbooked/', views.book_appointment, name="bookappointment"),
    path('appointmentcancelled<int:pid>&<int:apt_id>/', views.cancel_appointment, name="cancelappointment"),
    path('appointmentcancelledbydoctor<int:pid>&<int:apt_id>/', views.cancel_appointment_doctor, name="cancelappointmentdoctor"),
    path('appointmentupdatedbydoctor/', views.update_appointment_doctor, name="updateaptbydoctor"),
    
    path('profileupdateddoctor/', views.update_doctor_profile, name="updateprofiledoctor"),
    path('doctordashboard/', views.doctordashboard)
]
