from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .models import Book

@login_required
def home(request):
    template_name = "library/home.html"
    ctx = {}
    books = Book.objects.all()
    
    if request.method == "GET":
        search_book = request.GET.get('search')
        if search_book != None:
            books = books.filter(title__contains=search_book) if books.filter(title__contains=search_book).exists() else books

    ctx.update({"books": books}) 

    return render(request, template_name, ctx)


@login_required
# @staff_member_required(login_url=settings.LOGIN_URL)
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
# @staff_member_required(login_url=settings.LOGIN_URL)
def dashboard_books(request):
    ctx = {}
    template_name = "library/dashboard.html"

    if request.method == "POST":
        ...
    else:
        ...
    
    return render(request, template_name, ctx)