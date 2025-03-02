from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from colorfield.fields import ColorField

# TODO: add doc


class Author(models.Model):
    photo = models.ImageField(
        verbose_name="Foto", upload_to="author-photos/", null=True, blank=True
    )

    first_name = models.CharField(
        verbose_name="Primeiro Nome", max_length=150, blank=True, null=True
    )

    last_name = models.CharField(
        verbose_name="Sobrenome", max_length=150, blank=True, null=True
    )

    biography = models.TextField(verbose_name="Biografia", null=True, blank=True)

    birth_date = models.DateField(
        verbose_name="Data de Nascimento", blank=True, null=True
    )

    death_date = models.DateField(verbose_name="Data de Óbito", blank=True, null=True)

    addition_date = models.DateTimeField(
        verbose_name="Data de adição",
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
    )

    slug = models.SlugField(blank=True, null=True, unique=True)

    @property
    def get_full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}".strip()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_full_name.lower())

        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name


class Publisher(models.Model):
    photo = models.ImageField(
        verbose_name="Foto", upload_to="publisher-photos", null=True, blank=True
    )
    name = models.CharField(verbose_name="Nome", max_length=255, unique=True)
    website = models.URLField(verbose_name="Website", blank=True, null=True)
    address = models.CharField(
        verbose_name="Endereço", max_length=50, blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Descrição", blank=True, null=True, max_length=150
    )

    def __str__(self):
        return self.name


# Better input a Multiple Choices Category in Book, it making it difficult to work
class Category(models.Model):
    name = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, blank=False, null=False
    )
    color = ColorField(default="#efefef", null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    LANGUAGE_CHOICES = [
        ("PT", "Português"),
        ("EN", "Inglês"),
    ]

    cover = models.ImageField(
        verbose_name="Capa", upload_to="cover-photos/", null=True, blank=True
    )

    title = models.CharField(
        verbose_name="Título", max_length=255, blank=False, null=False
    )

    authors = models.ManyToManyField(
        to=Author,
        related_name="books",
    )

    summary = models.TextField(verbose_name="Resumo", null=True, blank=True)

    isbn = models.CharField(verbose_name="ISBN", unique=True, max_length=13)

    publisher = models.ForeignKey(
        to=Publisher, related_name="books", on_delete=models.CASCADE
    )

    categories = models.ManyToManyField(
        to=Category,
        related_name="books",
    )

    publication_date = models.DateField(
        verbose_name="Data de Publicação",
    )

    document = models.FileField(
        verbose_name="Documento", upload_to="books/", null=True, blank=True
    )

    created_at = models.DateTimeField(
        verbose_name="Data de criação", auto_now_add=True, editable=False
    )

    language = models.CharField(
        verbose_name="Idioma", max_length=2, choices=LANGUAGE_CHOICES, default="PT"
    )

    pages = models.PositiveIntegerField(verbose_name="Páginas", null=True, blank=True)

    edition = models.PositiveIntegerField(
        verbose_name="Edição",
        null=True,
        blank=True,
        help_text="Por padrão o sistema registra como a primeira edição livro",
    )

    slug = models.SlugField(unique=True, editable=False, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.isbn}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Sugestion(models.Model):
    user = models.ForeignKey(
        verbose_name="sugestion", to=User, on_delete=models.CASCADE
    )
    about = models.CharField(verbose_name="Assunto", max_length=50)
    text = models.TextField(verbose_name="Sugestão", max_length=500)
    date_sugested = models.DateTimeField(verbose_name="data", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.date_sugested})"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        related_name="books_comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
