from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from .models import Book, Author, Category, Publisher
from .forms import BookForm, AuthorForm, CategoryForm, PublisherForm


@login_required
def home(request):  
    ctx = {}
    template_name = "library/home.html"

    ctx["books"] = Book.objects.all()
    return render(request, template_name, ctx)


@login_required
@staff_member_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    ctx = {}
    template_name = "library/dashboard.html"
    books = Book.objects.all()

    ctx["books"] = books
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
def get_book_data(request, slug):
    book = get_object_or_404(Book, slug=slug)

    return JsonResponse({
        'cover': book.cover.url,
        'title': book.title,
        'summary': book.summary,
        'pages': book.pages,
        'language': book.get_language_display(),
        'categories': [category.name for category in book.categories.all()],
        'authors': [author.get_full_name for author in book.authors.all()],
        'isbn': book.isbn,
        'publisher': book.publisher.name,
        'publication_date': book.publication_date,
        'edition': book.edition
    })