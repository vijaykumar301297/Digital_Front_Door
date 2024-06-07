import random
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
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt

from doctor_users.models import ScheduleTime
from hms import settings
from django.utils.encoding import force_bytes, force_str
from admin_user.tokens import account_activation_token
from authentication.models import UserAuthentication
from department.models import Department
from doctor_users.decorators import unauthorized_user, allowed_users, admin_users
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

from patientbooking.models import Patient


# Create your views here.

@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def create_staff_user(request):
    dept_data = Department.objects.all()

    if request.method == 'POST':
        print(request.method)
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        education = request.POST['education']
        # department = request.POST['department_id']
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
            return redirect('stafflist')
        else:
            user = UserAuthentication(username=username, first_name=firstname, last_name=lastname, email=email,
                                      gender=gender, phone_number=phone_number, address=address,
                                      date_of_birth=date_of_birth, joining_date=joining_date, about=about,
                                      password=password, role=role, designation=designation,
                                      account_status='Invited', img=img, language_known=language_known,
                                      education=education)

            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Staff')
            user.groups.add(group)

            current_site = get_current_site(request)
            email_subject = "Doctor Confirmation Mail"
            message2 = render_to_string('staff/mail.html', {
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

            return redirect('stafflist')

    return render(request, 'staff/addstaff.html',
                  {'dept_data': dept_data, 'media_url': settings.MEDIA_URL, 'navbar': 'create-staff'})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def activate_user(request, uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserAuthentication.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
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
def staff_list(request):
    staff_data = UserAuthentication.objects.all().filter(role='Staff').order_by('id')

    p = Paginator(staff_data, 1)
    page = request.GET.get("page", 1)
    datas = p.get_page(page)

    return render(request, 'staff/stafflist.html', {'data': datas, 'staff_data': staff_data, 'navbar': 'staff-list'})


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def edit_staff(request, id):
    dept_data = Department.objects.all()
    staff_data = UserAuthentication.objects.get(pk=id)
    context = {
        'staff_data': staff_data,
        'dept_data': dept_data,
        'navbar': 'edit-staff'
    }

    if request.method == 'POST':
        staff_data.first_name = request.POST['first_name']
        staff_data.last_name = request.POST['last_name']
        staff_data.designation = request.POST['designation']
        staff_data.education = request.POST['education']
        # staff_data.department_id = request.POST['department_id']
        staff_data.phone_number = request.POST['phone_number']
        staff_data.language_known = request.POST['language_known']
        staff_data.address = request.POST['address']
        staff_data.about = request.POST['about']
        staff_data.save()

        return redirect('stafflist')

    return render(request, 'staff/editstaff.html', context)


# @permission_required()
@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def del_staff(request, id):
    staff_data = UserAuthentication.objects.get(pk=id)
    context = {
        'staff_data': staff_data,
        'navbar': 'delete-staff'
    }

    if request.method == 'POST':
        print(request.method)
        staff_data = request.POST.getlist('id[]')
        # print(doct_data.query)

        if len(staff_data) >= 1:
            for id_no in staff_data:
                del_doct = UserAuthentication.objects.get(pk=id_no)
                del_doct.delete()
            return redirect('stafflist')
        else:
            staff_data.delete()
            return redirect('stafflist')

    return render(request, 'staff/deleteastaff.html', context)


@allowed_users(allowed_roles='Staff')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def patient_appointment(request):
    pa = Patient.objects.all()
    paginator = Paginator(pa, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'booking/appointment.html', {'pa': pa, 'datas': data, 'navbar': 'appointment'})


@allowed_users(allowed_roles='Staff')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def patient(request):
    patient = Patient.objects.all()
    paginator = Paginator(patient, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'staff/patient.html', {'pa': patient, 'datas': data, 'navbar': 'patients'})


@allowed_users(allowed_roles='Staff')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def schedule_list(request):
    schedule_list = ScheduleTime.objects.all()
    paginator = Paginator(schedule_list, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'staff/doctor_schedule.html',
                  {'schedule_list': schedule_list, 'data': data, 'navbar': 'Doctor-schedule'})


@allowed_users(allowed_roles='Staff')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@csrf_exempt
def book_patient_offline(request):
    user = UserAuthentication.objects.all().filter(role='Doctor')
    dept = Department.objects.all()
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        dob = request.POST['date_of_birth']
        gender = request.POST['gender']
        doctor_name = request.POST['user_id']
        specialization = request.POST['specialization']
        location = request.POST['location']
        dates = request.POST['date']
        appointed_date = request.POST['appointed_date']

        doc = UserAuthentication.objects.all().get(id=doctor_name)

        data = Patient(full_name=full_name, phone_number=phone_number, date_of_birth=dob, email=email,
                       gender=gender, user_id=doc, specialization=specialization, location=location,
                       dates=dates, appointed_date=appointed_date)

        email_subject = "HMS Appointment Mail"
        message2 = render_to_string('booking/mail.html', {
            'name': data.full_name,
            'doctor': doc.first_name,
            'date': data.dates,
            'time': data.appointed_date,

        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST,
            [data.email],
        )
        email.fail_silently = True
        email.send()

        data.save()
        return redirect('patient')

    return render(request, 'staff/patient_book_online.html', {'doctor': user, 'dept': dept, 'navbar': 'add-patient'})

