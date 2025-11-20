from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.models import Department, Role

def is_super_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_super_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})

@login_required
@user_passes_test(is_super_admin)
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        password = request.POST.get("password", "")
        department_id = request.POST.get("department", "")
        role_id = request.POST.get("role", "")
        phone = request.POST.get("phone", "").strip()
        
        errors = {}

        if not username:
            errors["username"] = "Username is required."
        if not first_name:
            errors["first_name"] = "First name is required."
        if not last_name:
            errors["last_name"] = "Last name is required."
        if not email:
            errors["email"] = "Email is required."
        elif "@" not in email:
            errors["email"] = "Invalid email format."
        if not phone:
            errors["phone"] = "Phone number is required."
        if not password:
            errors["password"] = "Password is required."
        elif len(password) < 6:
            errors["password"] = "Password must be at least 6 characters."
        if not department_id:
            errors["department"] = "Department is required."
        if not role_id:
            errors["role"] = "Role is required."

        if User.objects.filter(username=username).exists():
            errors["username"] = "This username is already taken."

        if User.objects.filter(email=email).exists():
            errors["email"] = "This email is already registered."

        department_obj = None
        role_obj = None

        if department_id:
            try:
                department_obj = Department.objects.get(pk=department_id)
            except Department.DoesNotExist:
                errors["department"] = "Selected department does not exist."

        if role_id:
            try:
                role_obj = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                errors["role"] = "Selected role does not exist."

        if errors:
            return render(request, "create_user.html", {
                "errors": errors,
                "form_data": request.POST,
                "roles": Role.objects.all(),
                "departments": Department.objects.all()
            })
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save() 

        profile = user.profile
        profile.phone = phone
        profile.department = department_obj
        profile.role = role_obj
        profile.save()

        messages.success(request, "User created successfully!")
        return redirect("accounts:user_list")

    roles = Role.objects.all()
    departments = Department.objects.all()
    return render(request, "create_user.html", {"roles": roles, "departments": departments})
@login_required
@user_passes_test(is_super_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments_list.html', {'departments': departments})

def create_department(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        
        errors = {}

        if not name:
            errors["name"] = "Department name is required."

        if Department.objects.filter(name=name).exists():
            errors["name"] = "This department already exists."

        if errors:
            return render(request, "create_department.html", {
                "errors": errors,
                "form_data": request.POST
            })
            
        Department.objects.create(name=name)

        messages.success(request, "Department created successfully!")
        return redirect("accounts:department_list")
    
    return render(request, "create_department.html")

@login_required
@user_passes_test(is_super_admin)
def roles(request):
    roles = Role.objects.all()
    return render(request, 'roles_list.html', {'roles': roles})

@login_required
@user_passes_test(is_super_admin)
def create_role(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        
        errors = {}

        if not name:
            errors["name"] = "Role name is required."

        if Role.objects.filter(name=name).exists():
            errors["name"] = "This role already exists."

        if errors:
            return render(request, "create_role.html", {
                "errors": errors,
                "form_data": request.POST
            })
            
        Role.objects.create(name=name)

        messages.success(request, "Role created successfully!")
        return redirect("accounts:role_list")
    
    return render(request, "create_role.html")

@login_required
@user_passes_test(is_super_admin)
def editUser(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect("accounts:user_list")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        department_id = request.POST.get("department", "")
        role_id = request.POST.get("role", "")
        
        errors = {}

        if not first_name:
            errors["first_name"] = "First name is required."
        if not last_name:
            errors["last_name"] = "Last name is required."
        if not email:
            errors["email"] = "Email is required."
        elif "@" not in email:
            errors["email"] = "Invalid email format."
        if not phone:
            errors["phone"] = "Phone number is required."

        if User.objects.filter(email=email).exclude(pk=user_id).exists():
            errors["email"] = "This email is already registered."

        department_obj = None
        role_obj = None

        if department_id:
            try:
                department_obj = Department.objects.get(pk=department_id)
            except Department.DoesNotExist:
                errors["department"] = "Selected department does not exist."

        if role_id:
            try:
                role_obj = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                errors["role"] = "Selected role does not exist."

        if errors:
            return render(request, "edit_user.html", {
                "errors": errors,
                "form_data": request.POST,
                "roles": Role.objects.all(),
                "departments": Department.objects.all(),
                "user_obj": user
            })

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile = user.profile
        profile.phone = phone
        profile.department = department_obj
        profile.role = role_obj
        profile.save()

        messages.success(request, "User updated successfully!")
        return redirect("accounts:user_list")

    roles = Role.objects.all()
    departments = Department.objects.all()
    return render(request, "edit_user.html", {
        "roles": roles,
        "departments": departments,
        "user_obj": user
    })
    
