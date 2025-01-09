from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test


def is_staff(user):
    if not user.is_staff:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    return True


just_staff_users = user_passes_test(is_staff)


@login_required
def home(request):
    template_name = "library/home.html"

    return render(request, template_name)


@login_required
@just_staff_users
def upload_books(request):
    ctx = {}
    template_name = "library/upload-books.html"

    if request.method == "POST":
        ...
    else:
        ...
    
    ctx["form"] = ""

    return render(request, template_name, ctx)


@login_required
@just_staff_users
def dashboard_books(request):
    ctx = {}
    template_name = "library/dashboard.html"

    if request.method == "POST":
        ...
    else:
        ...
    
    return render(request, template_name, ctx)