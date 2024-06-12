from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.core.mail import send_mail, EmailMessage
from django.utils.html import strip_tags
from django.core.paginator import Paginator

from doctor_users.decorators import allowed_users
from authentication.models import UserAuthentication
from hms import settings
from .models import Patient
from department.models import Department
from doctor_users.models import ScheduleTime
from django.db.models import Q
from django.core import serializers
from datetime import datetime

# import datetime

# from .forms import PatientForm

start_date = datetime.today()
end_date = datetime.today()


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@csrf_exempt
def book(request):
    location = ScheduleTime.objects.all().values('location').distinct()
    department = Department.objects.all()
    print(department)
    #
    if request.method == 'POST':
        locations = request.POST['location']
        department_data = request.POST['department']
        print(department_data)
        selected_date = request.POST['selected_date']
        print(selected_date)

        data = ScheduleTime.objects.all().filter(Q(location=locations) & Q(deptId_id=department_data) &
                                                 Q(date=selected_date))
        print(data)
        if len(data) == 0:
            messages.error(request, 'Doctors were not available')
            return redirect('book')
        # print(data.query)

        else:
            department_id = Department.objects.all().filter(pk=department_data)
            print(department_id)
            user = UserAuthentication.objects.all().filter(pk__in=data.values_list('user_id_id', flat=True))
            return render(request, 'booking/book_slot.html', {'data': data, 'user': user, 'locations': locations,
                                                              'location': location, 'department_data': department_id,
                                                              'selected_date': selected_date, 'department': department})

    return render(request, 'booking/book.html', {'location': location, 'department': department})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@csrf_exempt
def ajax_call(request):
    if request.method == 'POST':
        selected_date = request.POST['date']
        location = request.POST['location']
        department = request.POST['department']
        print(selected_date)
        get_data = ScheduleTime.objects.all().filter(Q(location=location) & Q(deptId_id=department) &
                                                     Q(date=selected_date))
        user_data = list(
            UserAuthentication.objects.all().filter(pk__in=get_data.values_list('user_id_id', flat=True)).values())
        scheduled_data = list(ScheduleTime.objects.all().filter(Q(location=location) & Q(deptId_id=department) &
                                                                Q(date=selected_date)).values())

        return JsonResponse({'data': scheduled_data, 'user_data': user_data})

    return JsonResponse({'status': 'error'})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@csrf_exempt
def book_patient(request):
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
        # payment = request.POST['payment']

        d = UserAuthentication.objects.all().get(id=doctor_name)

        data = Patient(full_name=full_name, phone_number=phone_number, date_of_birth=dob, email=email,
                       gender=gender, user_id=d, specialization=specialization, location=location,
                       dates=dates, appointed_date=appointed_date)

        email_subject = "HMS Appointment Mail"
        message2 = render_to_string('booking/mail.html', {
            'name': data.full_name,
            'doctor': d.first_name,
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
        return redirect(book)

    return render(request, 'booking/patient_book.html')


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def patient_appointment(request):
    pa = Patient.objects.all().filter(dates__gte=start_date)
    paginator = Paginator(pa, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    print(pa)
    return render(request, 'booking/appointment.html', {'pa': pa, 'datas': data, 'navbar': 'appointmets-lists'})


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def patient(request):
    patient = Patient.objects.all()
    paginator = Paginator(patient, 5)
    page = request.GET.get("page")
    data = paginator.get_page(page)

    return render(request, 'booking/patient.html', {'pa': patient, 'datas': data, 'navbar': 'patient-lists'})


@allowed_users(allowed_roles='Admin')
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

    return render(request, 'booking/patient_book_online.html', {'doctor': user, 'dept': dept, 'navbar': 'book'})


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def del_appointment(request, id):
    pa = Patient.objects.all().filter(pk=id)

    if request.method == 'POST':
        print(request.method)
        del_sche = Patient.objects.get(pk=id)
        del_sche.delete()
        return redirect('appointment')
    return render(request, 'booking/deleteappointment.html', {'pa': pa})


@allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def del_patient(request, id):
    pa = Patient.objects.all().filter(pk=id)

    if request.method == 'POST':
        print(request.method)
        del_sche = Patient.objects.get(pk=id)
        del_sche.delete()
        return redirect('appointment')
    return render(request, 'booking/deletepatient.html', {'pa': pa, 'navbar': 'delete'})
