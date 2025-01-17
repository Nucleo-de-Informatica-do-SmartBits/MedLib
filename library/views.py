from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from .models import Book, Author, Category, Publisher, Sugestion
from .forms import BookForm, AuthorForm, CategoryForm, PublisherForm, SugestionForm
from django.contrib import messages


@login_required
def home(request):  
    ctx = {}
    template_name = "library/home.html"
    ctx = {}
    books = Book.objects.all()
    
    if request.method == "GET":
        search_book = request.GET.get('search')
        if search_book != None:
            if books.filter(title__contains=search_book).exists():
                books = books.filter(title__contains=search_book)
            # elif books.filter(categories__contains=search_book).exists():
            #     books = books.filter(categories__contains=search_book) -> Error in MenyToMeny field, I hate this Relation from django 

    ctx.update({"books": books}) 

    return render(request, template_name, ctx)


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    ctx = {}
    template_name = "library/dashboard.html"
    books = Book.objects.all()
    sugestions = Sugestion.objects.all()

    ctx["books"] = books
    ctx["sugestions"] = sugestions
    ctx["total_books"] = books.count()
    ctx["total_authors"] = Author.objects.all().count()
    ctx["total_categories"] = Category.objects.all().count()
    ctx["total_publishers"] = Publisher.objects.all().count()
    return render(request, template_name, ctx)


@login_required
@require_http_methods(["DELETE"])
def deleteBook(request, slug):
    ctx = {}
    partial_name = "partials/dashboard-table-books.html"

    book = get_object_or_404(Book, slug=slug)
    book.delete()

    ctx["books"] = Book.objects.all()
    return render(request, partial_name, ctx)


@login_required
def addBook(request):
    ctx = {}
    template_name = "library/book-add.html"

    if request.method == "POST":
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book_form.save()

            return redirect("dashboard")
    else:
        book_form = BookForm()

    ctx["book_form"] = book_form
    ctx["title"] = "Carregar Livro"
    return render(request, template_name, ctx)


@login_required
def updateBook(request, slug):
    ctx = {}
    template_name = "library/book-add.html"
    instance = get_object_or_404(Book, slug=slug)

    if request.method == "POST":
        book_form = BookForm(request.POST, instance=instance)

        if book_form.is_valid():
            book_form.save()

            return redirect("dashboard")
    else:
        book_form = BookForm(instance=instance)

    ctx["book_form"] = book_form
    ctx["title"] = "Modificar Livro"
    return render(request, template_name, ctx)


@login_required
def bookDetails(request, slug):
    ctx = {}
    template_name = "library/book-details.html"
    book = get_object_or_404(Book, slug=slug)

    ctx["book"] = book
    return render(request, template_name, ctx)


@login_required
def sugest(request):
    template_name = "library/sugestion-form.html"
    ctx = {}

    if request.method == "POST":
        forms = SugestionForm(data=request.POST, request=request)
        if forms.is_valid():
            forms.save()
            messages.success(request=request, message="Sugestão Enviada com sucesso, Obrigado!")
            return redirect(to='sugestion')
    else:
        forms = SugestionForm()
    ctx.update({"forms": forms})
    return render(request=request, template_name=template_name, context=ctx)