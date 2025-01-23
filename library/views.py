from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods

from .forms import BookForm, SugestionForm
from .models import Author, Book, Category, Publisher, Sugestion


@login_required
def home(request):
    ctx = {}
    template_name = "library/home.html"
    books = Book.objects.all()

    # I'll solve this later
    # if request.method == "GET":
    #     search_book = request.GET.get('search')
    #     if search_book != None:
    #         if books.filter(title__contains=search_book).exists():
    #             books = books.filter(title__contains=search_book)
    #         # elif books.filter(categories__contains=search_book).exists():
    #         #     books = books.filter(categories__contains=search_book) -> Error in MenyToMeny field, I hate this Relation from django

    ctx["books"] = books
    return render(request, template_name, ctx)


@login_required
def dashboard(request):
    ctx = {}
    template_name = "library/dashboard.html"

    if not request.user.is_staff:
        messages.info(request, "Você não tem permissão para acessar essa página")
        return redirect("home")

    books = Book.objects.all()
    sugestions = Sugestion.objects.all()

    ctx.update(
        {
            "books": books,
            "sugestions": sugestions,
            "total_books": books.count(),
            "total_authors": Author.objects.count(),
            "total_categories": Category.objects.count(),
            "total_publishers": Publisher.objects.count(),
        }
    )
    return render(request, template_name, ctx)


@login_required
@require_http_methods(["DELETE"])
def deleteBook(request, slug):
    ctx = {}
    partial_name = "partials/dashboard-table-books.html"

    book = get_object_or_404(Book, slug=slug)
    book.delete()

    ctx["books"] = Book.objects.all()

    messages.success(request, "Livro deletado com sucesso!")
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
def sugest(request):
    template_name = "library/sugestion-form.html"
    ctx = {}

    if request.method == "POST":
        forms = SugestionForm(data=request.POST, request=request)
        if forms.is_valid():
            forms.save()
            messages.success(
                request=request, message="Sugestão Enviada com sucesso, Obrigado!"
            )
            return redirect(to="sugestion")
    else:
        forms = SugestionForm()
        
    ctx.update({"forms": forms})
    return render(request=request, template_name=template_name, context=ctx)


@login_required
def getBookData(request, slug):
    book = get_object_or_404(Book, slug=slug)

    return JsonResponse(
        {
            "cover": book.cover.url if book.cover else "",
            "title": book.title,
            "summary": book.summary,
            "pages": book.pages,
            "language": book.get_language_display(),
            "categories": [category.name for category in book.categories.all()],
            "authors": [[author.photo.url, author.get_full_name] for author in book.authors.all()],
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
