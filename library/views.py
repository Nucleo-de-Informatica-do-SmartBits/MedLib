import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth import get_user
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods

from .forms import BookForm
from .models import Author, Book, Category, Publisher, Sugestion, Comment


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
def bookDetails(request, slug, isbn):
    ctx = {}
    template_name = "library/book-details.html"
    book = get_object_or_404(Book, slug=slug, isbn=isbn)

    ctx["book"] = book
    return render(request, template_name, ctx)


@login_required
@require_http_methods(["POST"])
def add_suggestion(request):
    try:
        data = json.loads(request.body)
        text = data.get("content")

        if not text:
            raise ValueError("O texto não pode estar vazio")

        Sugestion.objects.create(text=text, user=request.user)

        return JsonResponse({}, status=200)
    except Exception as error:
        return JsonResponse({"error": error}, 400)


@login_required
@require_http_methods(["POST"])
def add_comment(request):
    data = json.loads(request.body)
    book_slug = data.get("book_slug")
    content = data.get("content")

    if not content:
        return JsonResponse({"error": "no content"}, status=400)

    if not book_slug:
        return JsonResponse({"error": "no book_slug"}, status=400)

    book = get_object_or_404(Book, slug=book_slug)
    user = get_user(request)

    comment = Comment.objects.create(user=user, book=book, content=content)

    return JsonResponse(
        {
            "userId": comment.user.id,
            "username": comment.user.username,
            "book": comment.book.slug,
            "content": comment.content,
            "created_at": naturaltime(comment.created_at),
        },
        status=201,
    )


@login_required
@xframe_options_exempt
def readBook(request, slug, isbn):
    ctx = {}
    template_name = "library/read.html"
    book = get_object_or_404(Book, slug=slug, isbn=isbn)

    ctx["book"] = book
    return render(request, template_name, ctx)


@login_required
@require_http_methods(["GET"])
def search_for_books(request):
    query = request.GET.get('q')
    
    books = Book.objects.filter(title__icontains=query).values(
        "id", "title", "isbn", "slug"
    )
    return JsonResponse(list(books), safe=False)
