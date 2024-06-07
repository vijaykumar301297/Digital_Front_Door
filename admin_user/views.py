import re
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, get_user_model, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
# from doctor_users.decorators import unauthorized_user, allowed_users, admin_users
from hms import settings
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from authentication.models import UserAuthentication
from department.models import Department
import random


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def admin_list(request):
    data = UserAuthentication.objects.all().filter(role='Admin').order_by('id')

    paginator = Paginator(data, 5)
    page = request.GET.get('page')
    datas = paginator.get_page(page)
    return render(request, 'users/adminlist.html', {'data': data, 'navbar': 'admin-list', 'datas': datas})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def create_user(request):
    depart = Department.objects.all()

    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password'].strip()
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
        user_name_create = firstname

        capital_letter = 1
        special_char = 1
        digits = 2
        username_len = 5
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
            return redirect('admin')

        elif UserAuthentication.objects.all().filter(username=username).exists():
            messages.error(request, 'Username Already available, Kindly proceed with login')
            return redirect('admin')
        elif len(password) < 8:
            messages.error(request, 'Password length should be minimum 8')
            return redirect('admin')
        else:
            admin_data = UserAuthentication(first_name=firstname, last_name=lastname, username=username, email=email,
                                            gender=gender, phone_number=phone_number, address=address,
                                            date_of_birth=date_of_birth, joining_date=joining_date, about=about,
                                            password=password, role=role,
                                            designation=designation,
                                            account_status='Invited', img=img, education=education)

            admin_data.set_password(password)
            admin_data.save()
            group = Group.objects.get(name='Admin')
            admin_data.groups.add(group)

            current_site = get_current_site(request)
            email_subject = "Admin Confirmation Mail"
            message2 = render_to_string('users/mail.html', {
                'name': admin_data.first_name,
                'password': '12345678',
                'role': admin_data.role,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(admin_data.pk)),
                'token': account_activation_token.make_token(admin_data)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST,
                [admin_data.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('admin')

    return render(request, 'users/admin.html',
                  {'dept': depart, 'media_url': settings.MEDIA_URL, 'navbar': 'create-admin'})


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
        user.account_status = 'Confirmed'

        user.save()
        auth_login(request, user)
        messages.success(request, 'Account Activated Successfully')
        return redirect('login')

    else:
        return HttpResponse('Activation link is invalid!')


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit_admin(request, id):
    user = UserAuthentication.objects.get(pk=id)
    context = {
        'user': user,
    }

    dept_data = Department.objects.all()
    user = UserAuthentication.objects.get(pk=id)
    context = {
        'user': user,
        'dept_data': dept_data,
        'navbar': 'edit-admin'
    }

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.designation = request.POST['designation']
        user.education = request.POST['education']
        # user.department_id = request.POST['department_id']
        user.phone_number = request.POST['phone_number']
        user.language_known = request.POST['language_known']
        user.address = request.POST['address']
        user.about = request.POST['about']

        user.save()

        return redirect('admin')

    return render(request, 'users/editadmin.html', context)


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def del_admin(request, id):
    admin_data = UserAuthentication.objects.get(pk=id)
    context = {
        'admin_data': admin_data,
        'navbar': 'delete-admin'
    }
    if request.method == 'POST':
        admin_data.delete()
        return redirect('admin')

    return render(request, 'users/deleteadmin.html', context)
