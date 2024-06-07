from django.http import HttpResponse
from django.shortcuts import redirect


def unauthorized_user(view_func):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return
        return view_func(request, *args, **kwargs)

    return wrapper_fun


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def user_decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = ''
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You don't have access to view or edit this page")

        return wrapper_func

    return user_decorator


def admin_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Admin':
            return view_func(request, *args, **kwargs)
        if group == 'Doctor':
            return redirect('')

        return wrapper_func
