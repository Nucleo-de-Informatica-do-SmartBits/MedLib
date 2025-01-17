from django.db import models
from django.utils.text import slugify

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

    full_name = models.CharField(max_length=200)

    @property
    def get_full_name(self):
        return f"{str(self.first_name).capitalize()} {str(self.last_name).capitalize()}".strip()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_full_name.lower())
        if not self.full_name:
            self.full_name = self.first_name+self.last_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=255, unique=True)
    website = models.URLField(verbose_name="Website", blank=True, null=True)
    address = models.CharField(
        verbose_name="Endereço", max_length=50, blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Descrição", blank=True, null=True, max_length=150
    )


class Category(models.Model):
    name = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, blank=False, null=False
    )


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

    edition = models.PositiveIntegerField(verbose_name="Edição", null=True, blank=True)

    slug = models.SlugField(unique=True, editable=False, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.isbn}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
