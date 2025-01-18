from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods

<<<<<<< HEAD
from .forms import BookForm
from .models import Author, Book, Category, Publisher
=======
from .models import Book, Author, Category, Publisher, Sugestion
from .forms import BookForm, AuthorForm, CategoryForm, PublisherForm, SugestionForm
from django.contrib import messages
>>>>>>> 5c3cb4b10f6c49db59d3f9bcdbf18d2cafab6f1c


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
def dashboard(request):
    if not request.user.is_staff:
        messages.info(request, "Você não tem permissão para acessar essa página")
        return redirect("home")

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

    messages.success(request, "Livro deletado com sucesso!")
    ctx["books"] = Book.objects.all()
    return render(request, partial_name, ctx)


@login_required
def manageBook(request, slug=None):
    if slug:
        book_instance = get_object_or_404(Book, slug=slug)
    else:
        book_instance = None

    if request.method == "POST":
        form = BookForm(data=request.POST, instance=book_instance, files=request.FILES)

        if form.is_valid() and form.is_multipart():
            form.save()
            action = "criado" if not book_instance else "atualizado"
            messages.success(request, f"O livro foi {action} com sucesso.")
            return redirect("home")
        else:
            messages.error(
                request, "Erro ao salvar o livro. Verifique os dados e tente novamente."
            )

    else:
        form = BookForm(instance=book_instance)

    ctx = {
        "form": form,
        "title": "Adicionar Livro" if not book_instance else "Editar Livro",
    }
    return render(request, "library/book-add.html", ctx)


@login_required
def bookDetails(request, slug):
    ctx = {}
    template_name = "library/book-details.html"
    book = get_object_or_404(Book, slug=slug)

    ctx["book"] = book
    return render(request, template_name, ctx)


@login_required
<<<<<<< HEAD
def getBookData(request, slug):
=======
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

@login_required
def get_book_data(request, slug):
>>>>>>> 5c3cb4b10f6c49db59d3f9bcdbf18d2cafab6f1c
    book = get_object_or_404(Book, slug=slug)

    return JsonResponse(
        {
            "cover": book.cover.url if book.cover else "",
            "title": book.title,
            "summary": book.summary,
            "pages": book.pages,
            "language": book.get_language_display(),
            "categories": [category.name for category in book.categories.all()],
            "authors": [author.get_full_name for author in book.authors.all()],
            "isbn": book.isbn,
            "publisher": book.publisher.name,
            "publication_date": book.publication_date,
            "edition": book.edition,
            "read_link": reverse("books-read", args=[book.slug]),
        }
    )


@login_required
@xframe_options_exempt
def readBook(request, slug):
    ctx = {}
    template_name = "library/read.html"
    book = get_object_or_404(Book, slug=slug)

    ctx["book"] = book
    return render(request, template_name, ctx)
