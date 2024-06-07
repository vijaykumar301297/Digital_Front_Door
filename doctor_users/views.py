import random

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from hms import settings
from django.utils.encoding import force_bytes, force_str
from admin_user.tokens import account_activation_token
from authentication.models import UserAuthentication
from department.models import Department
from patientbooking.models import Patient
from .decorators import unauthorized_user, allowed_users, admin_users
from .models import ScheduleTime
from django.contrib.auth.models import Group


# Create your views here.

@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def create_user(request):
    dept_data = Department.objects.all()

    if request.method == 'POST':
        print(request.method)
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        education = request.POST['education']
        department = request.POST['department_id']
        designation = request.POST['designation']
        img = request.FILES['img']
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        date_of_birth = request.POST['date_of_birth']
        about = request.POST['about']
        joining_date = request.POST['joining_date']
        language_known = request.POST['language_known']

        user_name_create = firstname

        capital_letter = 1
        special_char = 1
        digits = 1
        username_len = 3
        special_chars = ['@']

        username = ""

        user_name_create = "".join(user_name_create.split())
        user_name_create = user_name_create.lower()

        min_char_from_name = username_len - digits - special_char

        temp = 0
        for i in range(random.randint(min_char_from_name, len(user_name_create))):
            if temp < capital_letter:
                username += user_name_create[i].upper()
                temp += 1

            else:
                username += user_name_create[i]

        temp_list = []

        for i in range(digits):
            temp_list.append(str(random.randint(0, 9)))

        for i in range(special_char):
            temp_list.append(special_chars[random.randint(0, len(special_chars) - 1)])

        random.shuffle(temp_list)

        username += "".join(temp_list)
        # print(username)

        if UserAuthentication.objects.all().filter(email=email).exists():
            messages.error(request, 'Email Already available, Kindly proceed with login')
            return redirect('doctor')
        else:
            user = UserAuthentication(username=username, first_name=firstname, last_name=lastname, email=email,
                                      gender=gender, phone_number=phone_number, address=address,
                                      date_of_birth=date_of_birth, joining_date=joining_date, about=about,
                                      password=password, role=role, department_id=department, designation=designation,
                                      account_status='Invited', img=img, language_known=language_known,
                                      education=education)

            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Doctor')
            user.groups.add(group)

            current_site = get_current_site(request)
            email_subject = "Doctor Confirmation Mail"
            message2 = render_to_string('doctor/mail.html', {
                'name': user.first_name,
                'password': '12345678',
                'role': user.role,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST,
                [user.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('doctor')

    return render(request, 'doctor/addDoctor.html',
                  {'dept_data': dept_data, 'media_url': settings.MEDIA_URL, 'navbar': 'create-doctor'})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def activate_user(request, uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserAuthentication.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_superuser = False
        user.account_status = 'Confirmed'
        user.save()
        login(request, user)

        return render(request, 'home.html')

    else:
        return HttpResponse('Activation link is invalid!')


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def doctor_list(request):
    doctor_data = UserAuthentication.objects.all().filter(role='Doctor').order_by('id')
    print(doctor_data)
    p = Paginator(doctor_data, 1)
    page = request.GET.get("page", 1)
    data = p.get_page(page)
    return render(request, 'doctor/doctorlist.html',
                  {'doctor_data': doctor_data, 'data': data, 'navbar': 'doctor-list'})


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def edit_doctor(request, id):
    dept_data = Department.objects.all()
    doctor_data = UserAuthentication.objects.get(pk=id)
    context = {
        'doctor_data': doctor_data,
        'dept_data': dept_data,
        'navbar': 'edit-doctor'
    }

    if request.method == 'POST':
        doctor_data.first_name = request.POST['first_name']
        doctor_data.last_name = request.POST['last_name']
        doctor_data.designation = request.POST['designation']
        doctor_data.education = request.POST['education']
        doctor_data.department_id = request.POST['department_id']
        doctor_data.phone_number = request.POST['phone_number']
        doctor_data.language_known = request.POST['language_known']
        doctor_data.address = request.POST['address']
        doctor_data.about = request.POST['about']
        doctor_data.save()

        return redirect('doctor')

    return render(request, 'doctor/edit_doctor.html', context)


# @permission_required()
@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def del_doctor(request, id):
    doct_data = UserAuthentication.objects.get(pk=id)
    context = {
        'doct_data': doct_data,
        'navbar': 'delete-doctor'
    }

    if request.method == 'POST':
        doct_data.delete()
        return redirect('doctor')

    return render(request, 'doctor/deletedoctor.html', context)


# Doctor page
@allowed_users(allowed_roles='Doctor')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def schedule_day(request, id):
    department = Department.objects.all()
    context = {
        'department': department,
    }
    if request.method == 'POST':
        dept_id = request.POST['deptId']
        date = request.POST['date']
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']
        location = request.POST['location']

        schedule = ScheduleTime(deptId_id=dept_id, date=date, from_time=from_time, to_time=to_time,
                                user_id_id=id, location=location)
        schedule.save()
        return redirect('list', id)

    return render(request, 'doctor/schedule.html', context)


@allowed_users(allowed_roles='Doctor')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def schedule_list(request, id):
    schedule_list = ScheduleTime.objects.all().filter(user_id_id=id)
    paginator = Paginator(schedule_list, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'doctor/doctor_schedule.html',
                  {'schedule_list': schedule_list, 'data': data, 'navbar': 'schedule-list'})


@allowed_users(allowed_roles='Doctor')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def edit_schedule(request, id):
    edit_schedule = ScheduleTime.objects.all().filter(pk=id)
    department = Department.objects.all()

    context = {
        'edit_schedule': edit_schedule,
        'department': department,
        'navbar': 'edit-schedule'
    }
    if request.method == 'POST':
        for i in edit_schedule:
            i.dept_id = request.POST['deptId']
            i.date = request.POST['date']
            i.from_time = request.POST['from_time']
            i.to_time = request.POST['to_time']
            i.location = request.POST['location']

            i.save()
            return redirect('list', i.user_id_id)

    return render(request, 'doctor/edit_schedule.html', context)


@allowed_users(allowed_roles='Doctor')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def delete_schedule(request, id):
    del_schedule = ScheduleTime.objects.all().filter(pk=id)

    if request.method == 'POST':
        print(request.method)
        del_sche = ScheduleTime.objects.get(pk=id)
        del_sche.delete()
        return redirect('list', del_sche.user_id_id)
    return render(request, 'doctor/deleteschedule.html', {'del_schedule': del_schedule, 'navbar': 'del-schedule'})


@allowed_users(allowed_roles='Doctor')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def patient_appointment(request, id):
    pa = Patient.objects.all().filter(user_id=id)
    paginator = Paginator(pa, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'booking/appointment.html', {'pa': pa, 'datas': data, 'navbar': 'appointment'})


@allowed_users(allowed_roles='Doctor')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def patient(request, id):
    patient = Patient.objects.all().filter(user_id=id)
    paginator = Paginator(patient, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'booking/patient.html', {'pa': patient, 'datas': data, 'navbar': 'patients'})
