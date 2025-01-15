from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from .models import Book
from .forms import BookForm, AuthorForm, CategoryForm, PublisherForm


@login_required
def home(request):
    template_name = "library/home.html"

    return render(request, template_name)


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
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
@staff_member_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    ctx = {}
    template_name = "library/dashboard.html"
    books = Book.objects.all()

    if request.method == "POST":
       book_form = BookForm(request.POST)

       if book_form.is_valid():
           book_form.save()
           return redirect("dashboard")
       
    else:
       book_form = BookForm()

    ctx["books"] = books
    ctx["book_form"] = book_form
    return render(request, template_name, ctx)


@login_required
@require_http_methods(["DELETE", "GET"])
def deleteBook(request, slug):
    book = get_object_or_404(Book, slug=slug)
    book.delete()

    return JsonResponse({"msg": "product deleted", "status": 200})


@login_required
def bookDetails(request, slug):
    ctx = {}
    template_name = "library/book-details.html"
    book = get_object_or_404(Book, slug=slug)

    ctx["book"] = book
    return render(request, template_name, ctx)
