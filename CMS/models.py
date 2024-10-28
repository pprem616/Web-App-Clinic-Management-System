from django.db import models
from datetime import date
from rest_framework import serializers



# Create your models here.
class Medicine(models.Model):
    p_id=models.BigIntegerField()
    m_name=models.CharField(max_length=100)
    m_mg=models.CharField(max_length=20,default="5 mg")
    m_duration=models.CharField(max_length=100,default="1 month")
    p_f_name=models.CharField(max_length=100,default="Master")
    p_l_name=models.CharField(max_length=100,default="master")
    date = models.DateField(default=date.today)
    comment=models.CharField(max_length=300,default="None")


class MedSerializer(serializers.Serializer):
    m_name=serializers.CharField(max_length=100)
    m_mg=serializers.CharField(max_length=20)
    m_duration=serializers.CharField(max_length=100)
    p_f_name=serializers.CharField(max_length=100)
    p_l_name=serializers.CharField(max_length=100)
    comment=serializers.CharField(max_length=300)
    p_id=serializers.IntegerField()

class Names(models.Model):
    f_names=models.CharField(max_length=255)
    l_names=models.CharField(max_length=255)

class Med_names(models.Model):
    med_names=models.CharField(max_length=1000)

class Med_names_Serializer(serializers.Serializer):
    med_names=serializers.CharField(max_length=1000)




class NameSerializer(serializers.Serializer):
    f_names=serializers.CharField(max_length=255)
    l_names=serializers.CharField(max_length=255)











class NewAppointment(models.Model):
    apt_id= models.AutoField(primary_key=True)
    pat_name= models.CharField(max_length=80)
    pid= models.IntegerField()
    gender= models.CharField(max_length=10)
    age = models.CharField(max_length=3)
    mobile_no = models.BigIntegerField()
    doc_spec= models.CharField(max_length=50)
    doc_name= models.CharField(max_length=80)
    apt_date= models.CharField(max_length=20)
    apt_time= models.CharField(max_length=20)
    book_date= models.CharField(max_length=20)
    book_time= models.CharField(max_length=20)
    status=models.CharField(max_length=30,default='Booked')
    remark=models.CharField(max_length=256,default=' ')


class DoctorDepartment(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=50)


class PatientRegister(models.Model):
    pid= models.AutoField(primary_key = True )
    first_name= models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25)
    gender= models.CharField(max_length=10)
    mobile_no= models.BigIntegerField()
    d_o_b = models.CharField(max_length=12)
    e_mail = models.CharField(max_length=50)
    pass_word= models.CharField(max_length=32)
    
   
class AdminAccount(models.Model):
    aid= models.AutoField(primary_key = True )
    username = models.CharField(max_length=25)
    e_mail = models.CharField(max_length=50)
    pass_word= models.CharField(max_length=32)

class DoctorAccount(models.Model):
    did= models.AutoField(primary_key = True )
    first_name= models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25)
    dept_id = models.IntegerField()
    depart_ment = models.CharField(max_length=50)
    gender= models.CharField(max_length=6)
    d_o_b = models.CharField(max_length=12)
    mobile_no= models.BigIntegerField()
    e_mail = models.CharField(max_length=50)
    pass_word= models.CharField(max_length=32)

class Contactus(models.Model):
    pname= models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


