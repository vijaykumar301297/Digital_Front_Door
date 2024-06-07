from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, get_user_model, logout
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from authentication.models import UserAuthentication


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def home(request):
    return render(request, 'base.html')


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            check_user = UserAuthentication.objects.filter(username=username).first()

            if check_user is not None:

                if check_user.account_status == 'Confirmed':
                    # if check_user.a
                    auth_login(request, user)
                    userdata = user.username
                    return redirect('home')

                elif check_user.account_status == 'Invited':
                    messages.error(request, 'Kindly, check the mail and activate the account')
                    return redirect('login')

            else:
                messages.error(request, 'Bad Credential')
                return redirect('login')

        else:
            messages.error(request, 'Bad Credential')
            return redirect('login')

    return render(request, 'authentication/base_auth.html')


def user_logout(request):
    logout(request)
    return redirect('login')
