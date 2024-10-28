import json
import hashlib
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contactus, PatientRegister, AdminAccount , DoctorAccount , DoctorDepartment , NewAppointment
from django.contrib import messages
from datetime import datetime
# Create your views here.



from django.shortcuts import render
from django.http import HttpResponse
from difflib import get_close_matches
from .models import Medicine,MedSerializer,NameSerializer,Names,Med_names_Serializer,Med_names
import json,random
from difflib import get_close_matches


# Create your views here.
def index(request):
    return render(request,"index.html")
def add_med(request):
    med_name=request.GET['name']
    med_mg=request.GET['mg']
    p_id=request.GET['id']
    comment=request.GET['m_message']
    duration=" "

    if(request.GET['AB']!='0'):
        duration+=request.GET['AB']+" "
    if(request.GET['AL']!='0'):
        duration+=request.GET['AL']+" "
    if(request.GET['AD']!='0'):
        duration+=request.GET['AD']+" "
    #print(duration)
    

    med_log= Medicine(m_name=med_name,m_mg=med_mg,p_id=p_id,m_duration=duration,comment=comment)
    try:
        med_log.save()
        return HttpResponse("true")
    except:
        return HttpResponse("False")
def get_med(request):
    medicines=[]
    p_medicine_list=[]
    meds=Medicine.objects.all()
    p_id=request.GET['p_id']
    for med in meds:
        ser=MedSerializer(med)
        medicines.append(ser.data)
    
    for i in range(len(medicines)):
        if(int(medicines[i]['p_id'])==int(p_id)):
            p_medicine_list.append(medicines[i])
    #print(p_medicine_list)

    return HttpResponse(json.dumps(p_medicine_list))
def data_mapper(request):
    names=[]
    close_match=[]
    id=request.GET['id']
    if(id=="med_name"):
        print("IN")
        a_names=Med_names.objects.all()
        for name in a_names:
            ser=Med_names_Serializer(name)
            names.append(ser.data)
        for i in names:
            close_match.append(i[id+'s'])
        t_names=set(get_close_matches(request.GET['data'], close_match))
        print(close_match)
        t_names=list(t_names)
        print(t_names)

        return HttpResponse(json.dumps(t_names))
    a_names=Names.objects.all()
    for name in a_names:
        ser=NameSerializer(name)
        names.append(ser.data)
    for i in names:
        close_match.append(i[id+'s'])

    t_names=set(get_close_matches(request.GET['data'], close_match))
    t_names=list(t_names)
    #print(t_names)
    return HttpResponse(json.dumps(t_names))
def create_prescription(request):
    p_ids=[]
    medicines=[]
    flag=0
    meds=Medicine.objects.all()
    for med in meds:
        ser=MedSerializer(med)
        medicines.append(ser.data)
    #print(medicines)
    for i in medicines:
        p_ids.append(i['p_id'])
    if(len(p_ids)>0):
        while(flag!=1):
            p_id=random.randint(100000000,999999999)
            if(p_id not in p_ids):
                flag=1
    else:
        p_id=random.randint(100000000,999999999)


    f_name=request.POST['first_name']
    l_name=request.POST['last_name']
    gender=request.POST['gender']
    return render(request,"prescription.html",{"f_name":f_name.capitalize(),"l_name":l_name.capitalize(),"gender":gender.capitalize(),"p_id":p_id})









def index(request):
    if request.method == "POST":
        if request.POST.get('login_e_mail') and request.POST.get('login_pass_word'):
            login_e_mail = request.POST.get('login_e_mail')
            login_pass_word = request.POST.get('login_pass_word') 
            profile = PatientRegister.objects.filter(e_mail = login_e_mail )
            deptobj = DoctorDepartment.objects.all()
            docobj = DoctorAccount.objects.all()
            for i in profile.values('pid'):
                appobj = NewAppointment.objects.filter(pid= i['pid'])
            if(PatientRegister.objects.filter(e_mail = login_e_mail,pass_word = login_pass_word).exists()):
                return render(request, 'patientdashboard.html',{ "userinfo": profile,"deptinfo":deptobj, "docinfo":docobj, "appinfo":appobj })
            else:
                messages.error(request,'Invalid E-mail & Password !')
                return render(request, 'index.html')


        elif request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('middle_name') and request.POST.get('mobile_no') and request.POST.get('d_o_b') and request.POST.get('e_mail') and request.POST.get('pass_word'):
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            middle_name = request.POST.get('middle_name')
            mobile_no = request.POST.get('mobile_no')
            d_o_b = request.POST.get('d_o_b')
            rev = d_o_b.split("-")
            dob = rev[2]+"/"+rev[1]+"/"+rev[0]
            e_mail = request.POST.get('e_mail')
            pass_word = request.POST.get('pass_word')
            gender = request.POST.get('gender')
            

            if PatientRegister.objects.filter(e_mail=e_mail).exists():
                messages.error(request,'Account already exists with that E-mail !')
                return render(request, 'index.html')
            else:
                addrecord = PatientRegister(first_name=first_name,last_name=last_name,middle_name=middle_name,mobile_no=mobile_no,d_o_b=dob,e_mail=e_mail,pass_word=pass_word,gender=gender)
                addrecord.save()
                messages.success(request,'Sign Up Successful !')
                return render(request, 'index.html')

        elif request.POST.get('admin_e_mail') and request.POST.get('admin_pass_word'):
            login_e_mail = request.POST.get('admin_e_mail')
            login_pass_word = request.POST.get('admin_pass_word')  
            profile = AdminAccount.objects.filter(e_mail = login_e_mail )
            patient = PatientRegister.objects.all()
            doctor = DoctorAccount.objects.all()
            appointment = NewAppointment.objects.all()
            dept = DoctorDepartment.objects.all()
            if(AdminAccount.objects.filter(e_mail = login_e_mail , pass_word = login_pass_word ).exists()):
                return render(request, 'admindashboard.html',{'userinfo':profile,'deptinfo':dept,'patinfo':patient,'docinfo':doctor, 'appinfo':appointment})
            else:
                messages.error(request,'Invalid E-mail & Password !')
                return render(request, 'index.html')

        elif request.POST.get('doctor_e_mail') and request.POST.get('doctor_password'):
            login_e_mail = request.POST.get('doctor_e_mail')
            login_pass_word = request.POST.get('doctor_password')  
            profile = DoctorAccount.objects.filter(e_mail = login_e_mail )

            if(DoctorAccount.objects.filter(e_mail = login_e_mail , pass_word = login_pass_word).exists()):
                doc_name = 'Dr. '
                x = DoctorAccount.objects.filter(e_mail=login_e_mail).values_list('first_name')
                y = DoctorAccount.objects.filter(e_mail=login_e_mail).values_list('last_name')
                doc_name = doc_name + (x[0][0]+' '+y[0][0])
                aptobj = NewAppointment.objects.filter(doc_name=doc_name)
                return render(request, 'doctodashboard.html',{"userinfo": profile,"appinfo":aptobj})
            else:
                messages.error(request,'Invalid E-mail & Password !')
                return render(request, 'index.html')

    else:
        return render(request, 'index.html')

def contact(request):
    if request.method == "POST":
        pname = request.POST.get('pname')
        email = request.POST.get('email')
        description = request.POST.get('description')
        query = Contactus(pname=pname,email=email,description=description)
        query.save()
        return render(request, 'index.html')
    else:
        return render(request, 'contact.html')

def update_profile(request):

    x = 0
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    middle_name = request.POST.get('middle_name')
    mobile_no = request.POST.get('mobile_no')
    d_o_b = request.POST.get('d_o_b')
    e_mail = request.POST.get('e_mail')
    pass_word = request.POST.get('pass_word')
    gender = request.POST.get('gender')
    profile = PatientRegister.objects.filter(e_mail = e_mail )
    deptobj = DoctorDepartment.objects.all()
    docobj = DoctorAccount.objects.all()
    for i in profile.values('pid'):
        x = i['pid']
        appobj = NewAppointment.objects.filter(pid= x)

    if request.method == 'POST':
        update = PatientRegister(pid=x,first_name=first_name,last_name=last_name,middle_name=middle_name,mobile_no=mobile_no,d_o_b=d_o_b,e_mail=e_mail,pass_word=pass_word,gender=gender)
        update.save()
        messages.success(request,'Your Profile is updated Successfully !')
        return render(request, 'patientdashboard.html',{ "userinfo": profile,"deptinfo":deptobj, "docinfo":docobj, "appinfo":appobj })
    else:
        return render(request, 'index.html')


def update_doctor_profile(request):

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    middle_name = request.POST.get('middle_name')
    mobile_no = request.POST.get('mobile_no')
    d_o_b = request.POST.get('d_o_b')
    e_mail = request.POST.get('e_mail')
    depart_ment = request.POST.get('depart_ment')
    pass_word = request.POST.get('pass_word')
    gender = request.POST.get('gender')

    i = DoctorAccount.objects.filter(e_mail= e_mail).values_list('did')
    x = i[0][0]
    j = DoctorAccount.objects.filter(e_mail= e_mail).values_list('dept_id')
    y = j[0][0]

    doc_name = 'Dr. '
    x1 = DoctorAccount.objects.filter(e_mail=e_mail).values_list('first_name')
    y1 = DoctorAccount.objects.filter(e_mail=e_mail).values_list('last_name')
    doc_name = doc_name + (x1[0][0]+' '+y1[0][0])

    aptobj = NewAppointment.objects.filter(doc_name=doc_name)

    profile = DoctorAccount.objects.filter(e_mail = e_mail )

    if request.method == 'POST':
        update = DoctorAccount(did=x,first_name=first_name,last_name=last_name,dept_id=y,middle_name=middle_name,mobile_no=mobile_no,depart_ment=depart_ment,d_o_b=d_o_b,e_mail=e_mail,pass_word=pass_word,gender=gender)
        update.save()
        messages.success(request,'Your Profile is updated Successfully !')
        return render(request, 'doctodashboard.html',{ "userinfo": profile, "appinfo":aptobj})
    else:
        return render(request, 'index.html')



def book_appointment(request):
    
    pat_name= request.POST.get("pat_name")
    pid= request.POST.get("pid")
    g = PatientRegister.objects.filter(pid = pid).values_list('gender')
    gender = g[0][0]
    m = PatientRegister.objects.filter(pid = pid).values_list('mobile_no')
    mobile_no = m[0][0]
    d = PatientRegister.objects.filter(pid = pid).values_list('d_o_b')
    k = datetime.now().date().strftime("%d/%m/%Y")
    i = d[0][0].split('/')
    age = int(k[6:]) - int(i[2]) 

    doc_spec = request.POST.get('doc_spec')
    dep_name =  DoctorDepartment.objects.values('dept_name').get(dept_id = doc_spec)

    doc_name = request.POST.get('doc_name')
    dr_name = 'Dr. '+ doc_name

    t = request.POST.get('apt_time')
    t = datetime.strptime(t, "%H:%M")
    apttime = t.strftime("%I:%M %p")

    apt_date = request.POST.get('apt_date')
    rev = apt_date.split("-")
    aptdate = rev[2]+"/"+rev[1]+"/"+rev[0]

    book_time = datetime.now().time().strftime("%I:%M %p")
    book_date = datetime.now().date().strftime("%d/%m/%Y")

   
    

    profile = PatientRegister.objects.filter(pid = pid )
    deptobj = DoctorDepartment.objects.all()
    docobj = DoctorAccount.objects.all()
    for i in profile.values('pid'):
        appobj = NewAppointment.objects.filter(pid= i['pid'])

    if request.method == "POST":
        book = NewAppointment(pat_name=pat_name, pid=pid, doc_spec=dep_name['dept_name'],doc_name=dr_name,apt_time=apttime,apt_date=aptdate,book_time=book_time,book_date=book_date,gender=gender,age=age,mobile_no=mobile_no)
        book.save()
        messages.success(request,'New appointment booked !')
        return render(request, 'patientdashboard.html', { "userinfo": profile,"deptinfo":deptobj, "docinfo":docobj, "appinfo":appobj})

def cancel_appointment(request,pid,apt_id):
    
    print(pid)
    print(apt_id)

    profile = PatientRegister.objects.filter(pid = pid)
    deptobj = DoctorDepartment.objects.all()
    docobj = DoctorAccount.objects.all()
    appobj = NewAppointment.objects.filter(pid= pid)

    x = NewAppointment.objects.filter(apt_id=apt_id).values_list()
    y = "Canceled by Patient"
    print(x)
    z = NewAppointment(apt_id=x[0][0],pat_name=x[0][1],pid=x[0][2],doc_spec=x[0][3],doc_name=x[0][4],apt_date=x[0][5],apt_time=x[0][6],book_date=x[0][7],book_time=x[0][8],status=y,remark='')
    z.save()
    messages.success(request,'You cancelled one of your appointment !')
    return render(request, 'patientdashboard.html', { "userinfo": profile,"deptinfo":deptobj, "docinfo":docobj, "appinfo":appobj})

def cancel_appointment_doctor(request,pid,apt_id):

    print(pid,apt_id)
    i = NewAppointment.objects.filter(apt_id= apt_id).values_list()
    
    dr_name = i[0][4]
    doc_name = dr_name[4:]
    doc_name= doc_name.split(' ')
    first_name = doc_name[0]
    last_name = doc_name[1]

    d = DoctorAccount.objects.filter(first_name= first_name, last_name= last_name).values_list('did')
    did = d[0][0]

    profile = DoctorAccount.objects.filter(did = did )
    patobj = PatientRegister.objects.filter(pid = pid)
    appobj = NewAppointment.objects.filter(doc_name=dr_name)

    x = NewAppointment.objects.filter(apt_id=apt_id).values_list()
    y = "Cancelled by doctor"
    print(x)
    z = NewAppointment(apt_id=x[0][0],pat_name=x[0][1],pid=x[0][2],doc_spec=x[0][3],doc_name=x[0][4],apt_date=x[0][5],apt_time=x[0][6],book_date=x[0][7],book_time=x[0][8],status=y,remark='')
    z.save()
    messages.success(request,'You cancelled one of your appointment !')
    return render(request, 'doctodashboard.html', { "userinfo": profile, "patinfo":patobj, "appinfo":appobj})


@csrf_exempt
def update_appointment_doctor(request):
    data=request.POST.get("data")
    dict_data=json.loads(data)
    for i in dict_data:
        x = NewAppointment.objects.filter(apt_id = i['apt_id']).values_list()
        print(x)
        s = i['status']
        r = i['remark']
        z = NewAppointment(apt_id=x[0][0],pat_name=x[0][1],pid=x[0][2],gender=x[0][3],age=x[0][4],mobile_no=x[0][5],doc_spec=x[0][6],doc_name=x[0][7],apt_date=x[0][8],apt_time=x[0][9],book_date=x[0][10],book_time=x[0][11],status=s,remark=r)
        z.save()
    return JsonResponse(True,safe=False)


@csrf_exempt
def add_department(request):
   
    dept_name = request.POST.get("deptname")

    add = DoctorDepartment(dept_name=dept_name)
    add.save()

    data = {
            "deptname":add.dept_name,
            "deptid":add.dept_id,
            }
    return JsonResponse(data,safe=False)

@csrf_exempt
def update_department(request):
    data=request.POST.get("data")
    dict_data=json.loads(data)
    try:
        for i in dict_data:
            department=DoctorDepartment.objects.get(pk=i['deptid'])
            department.dept_name=i['deptname']
            department.save()
        return JsonResponse(True,safe=False)
    except:
        return JsonResponse(True,safe=False)

@csrf_exempt
def delete_department(request):
    dept_id=request.POST.get("id")
    deppartment=DoctorDepartment.objects.get(pk=dept_id)
    deppartment.delete()
    return JsonResponse(True,safe=False)



@csrf_exempt
def add_doctor(request):
   
    first_name = request.POST.get("firstname")
    last_name = request.POST.get("lastname")
    middle_name = request.POST.get("middlename")
    print(middle_name)
    depart_ment = request.POST.get("department")
    print(depart_ment)
    mobile_no = request.POST.get("mobileno")
    d_o_b = request.POST.get("dob") 
    e_mail = request.POST.get("email")
    pass_word = request.POST.get("password")
    gender = request.POST.get("gender")
    
    x = DoctorDepartment.objects.filter(dept_name= depart_ment).values_list('dept_id')
    deptid = x[0][0]

    add = DoctorAccount(first_name=first_name,last_name=last_name,middle_name=middle_name,dept_id=deptid,depart_ment=depart_ment,mobile_no=mobile_no,d_o_b=d_o_b,e_mail=e_mail,pass_word=pass_word,gender=gender)
    add.save()
    data = {
            "firstname":add.first_name,
            "lastname":add.last_name,
            "middlename":add.middle_name,
            "department":add.depart_ment,
            "mobileno":add.mobile_no,
            "dob":add.d_o_b,
            "email":add.e_mail,
            "password":add.pass_word,
            "gender":add.gender,
            "did":add.did
            }
    return JsonResponse(data,safe=False)

@csrf_exempt
def update_doctor(request):
    data=request.POST.get("data")
    dict_data=json.loads(data)
    try:
        for i in dict_data:
            doctor = DoctorAccount.objects.get(pk=i['did'])
            doctor.did = i['did']
            doctor.first_name=i['firstname']
            doctor.middle_name=i['middlename']
            doctor.depart_ment=i['department']
            doctor.last_name=i['lastname']
            doctor.d_o_b=i['dob']
            doctor.gender=i['gender']
            doctor.mobile_no=i['mobileno']
            doctor.e_mail=i['email']
            doctor.save()
        return JsonResponse(True,safe=False)
    except:
        return JsonResponse(True,safe=False)


@csrf_exempt
def delete_doctor(request):
    did=request.POST.get("id")
    doctor=DoctorAccount.objects.get(pk=did)
    doctor.delete()
    return JsonResponse(True,safe=False)



@csrf_exempt
def add_patient(request):
   
    first_name = request.POST.get("firstname")
    last_name = request.POST.get("lastname")
    middle_name = request.POST.get("middlename")
    mobile_no = request.POST.get("mobileno")
    d_o_b = request.POST.get("dob") 
    e_mail = request.POST.get("email")
    pass_word = request.POST.get("password")
    gender = request.POST.get("gender")

    add = PatientRegister(first_name=first_name,last_name=last_name,middle_name=middle_name,mobile_no=mobile_no,d_o_b=d_o_b,e_mail=e_mail,pass_word=pass_word,gender=gender)
    add.save()
    data = {
            "firstname":add.first_name,
            "lastname":add.last_name,
            "middlename":add.middle_name,
            "mobileno":add.mobile_no,
            "dob":add.d_o_b,
            "email":add.e_mail,
            "password":add.pass_word,
            "gender":add.gender,
            "pid":add.pid
            }
    return JsonResponse(data,safe=False)

@csrf_exempt
def update_patient(request):
    data=request.POST.get("data")
    dict_data=json.loads(data)
    try:
        for i in dict_data:
            patient=PatientRegister.objects.get(pk=i['pid'])
            patient.pid = i['pid']
            patient.first_name=i['firstname']
            patient.middle_name=i['middlename']
            patient.last_name=i['lastname']
            patient.d_o_b=i['dob']
            patient.gender=i['gender']
            patient.mobile_no=i['mobileno']
            patient.e_mail=i['email']
            patient.save()
        return JsonResponse(True,safe=False)
    except:
        return JsonResponse(True,safe=False)


@csrf_exempt
def delete_patient(request):
    pid=request.POST.get("id")
    patient=PatientRegister.objects.get(pk=pid)
    patient.delete()
    return JsonResponse(True,safe=False)


def remove_doctor(request,did,aid):
    DoctorAccount.objects.filter(did=did).delete()
    messages.success(request,'Doctor removed successfully !')
    
    profile = AdminAccount.objects.filter(aid = aid )
    patient = PatientRegister.objects.all()
    doctor = DoctorAccount.objects.all()
    appointment = NewAppointment.objects.all()
    return render(request, 'admindashboard.html',{'userinfo':profile,'patinfo':patient,'docinfo':doctor, 'appinfo':appointment})

def remove_appointment(request,pid,aid):
    NewAppointment.objects.filter(apt_id=aid).delete()
    messages.success(request,'Appointment removed successfully !')

    profile = AdminAccount.objects.filter(aid = aid )
    patient = PatientRegister.objects.all()
    doctor = DoctorAccount.objects.all()
    appointment = NewAppointment.objects.all()
    return render(request, 'admindashboard.html',{'userinfo':profile,'patinfo':patient,'docinfo':doctor, 'appinfo':appointment})

def about(request):
    return render(request, 'about.html')

def patientdashboard(request):
    return render(request, 'patientdashboard.html')

def admindashboard(request):
    return render(request, 'admindashboard.html')

def doctordashboard(request):
    return render(request, 'doctordashboard.html')
