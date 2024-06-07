from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from authentication.models import UserAuthentication
from django.contrib import messages
import re


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def account_setting(request):
    user_data = request.user
    user = UserAuthentication.objects.get(pk=user_data.id)
    if request.method == 'POST':
        user.phone_number = request.POST['phone_number']
        user.address = request.POST['address']
        user.education = request.POST['education']
        user.experience = request.POST['experience']
        user.about = request.POST['about']
        user.language_known = request.POST['language_known']
        user.location = request.POST['location']
        user.linkedin = request.POST['linkedin']
        user.save()

        return redirect('account_info', id)

    return render(request, 'setting/account_setting.html', {'user': user, 'navbar':'edit-account-info'})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def account_info(request):
    user_data = request.user
    change_user = UserAuthentication.objects.get(pk=user_data.id)
    return render(request, 'setting/account_info.html', {'change_user': change_user, 'navbar':'account-info'})


@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def password_update(request):
    if request.method == 'POST':
        user_data = request.user
        print(user_data)
        old = request.POST['old_password']
        new = request.POST['new_password']
        password = request.POST['password']

        if not check_password(old, user_data.password):
            messages.error(request, 'Old password not matched, kindly enter the correct password or'
                                    ' Go to main page to reset password')
            return redirect('password_change')
        else:
            if new == password:
                if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-+]).{8,}$', password):
                    if check_password(password, user_data.password):
                        messages.error(request, 'Password should not be same as old password')
                        return redirect('password_change')
                    else:
                        user_data.set_password(password)
                        user_data.save()
                        return redirect('home')
                else:
                    messages.error(request, 'Passwords should contain a capital letter, a small letter, a special '
                                            'character, a number, and a length of at least 8 letters.')
                    return redirect('password_change')
            else:
                messages.error(request, 'Password not matching, kindly check the new and confirm password')
                return redirect('password_change')

    return render(request, 'setting/passwordsetting.html', {'navbar': 'change-password'})
