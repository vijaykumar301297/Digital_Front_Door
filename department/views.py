from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from .models import Department
from django.contrib import messages


# from doctordetails.decorators import allowed_users


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
@login_required(login_url='login')
def create_department(request):
    if request.method == 'POST':
        department_name = request.POST['department_name']
        department_no = request.POST['department_no']
        department_head = request.POST['department_head']
        department_date = request.POST['department_date']
        department_status = request.POST['department_status']
        department_info = request.POST['department_info']

        if department_name == '':
            messages.error(request, 'Enter Department name')
            return render(request, 'department/department.html')

        elif Department.objects.all().filter(department_name=department_name).exists():
            messages.error(request, 'Department Already Available')
            return render(request, 'department/department.html')

        else:
            department_data = Department(department_name=department_name, department_no=department_no,
                                         department_head=department_head, department_date=department_date,
                                         department_status=department_status, department_info=department_info)

        department_data.save()
        return redirect('department_list')

    return render(request, 'department/department.html', {'navbar': 'department',})


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def department_list(request):
    department_data = Department.objects.all()
    paginator = Paginator(department_data, 3)
    page = request.GET.get('page')
    data = paginator.get_page(page)

    return render(request, 'department/departmentlist.html', {
        'department': department_data,
        "navbar": 'department-list',
        'datas': data,
    })


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def edit_department(request, id):
    department_data = Department.objects.get(pk=id)

    context = {
        'department_data': department_data,
        'navbar': 'edit-department',
    }
    if request.method == 'POST':
        department_data.department_name = request.POST['department_name']
        department_data.department_no = request.POST['department_no']
        department_data.department_head = request.POST['department_head']
        department_data.department_date = request.POST['department_date']
        department_data.department_status = request.POST['department_status']
        department_data.department_info = request.POST['department_info']
        department_data.save()

        return redirect('department_list')

    return render(request, 'department/edit_department.html', context)


# @allowed_users(allowed_roles='Admin')
@ensure_csrf_cookie
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@csrf_protect
def del_department(request, id):
    dept_data = Department.objects.get(pk=id)
    context = {
        'dept_data': dept_data,
        'navbar': 'delete-department',
    }

    if request.method == 'POST':
        dept_data.delete()
        return redirect('department_list')

    return render(request, 'department/deletedepartment.html', context)
