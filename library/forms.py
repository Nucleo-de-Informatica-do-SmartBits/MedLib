import datetime

from django import forms

from .models import Author, Book, Category, Publisher, Sugestion
from django.contrib.auth.models import User
from django.utils import timezone



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ["slug"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        exclude = ["slug"]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "cover",
            "title",
            "authors",
            "summary",
            "isbn",
            "publisher",
            "categories",
            "publication_date",
            "document",
            "language",
            "pages",
            "edition",
        ]
        widgets = {
            "cover": forms.ClearableFileInput(
                attrs={
                    "class": "w-full text-gray-400 text-sm bg-white border file:cursor-pointer cursor-pointer file:border-0 file:py-3 file:px-4 file:mr-4 file:bg-gray-100 file:hover:bg-gray-200 file:text-gray-800 rounded"
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500",
                    "placeholder": "Digite o título do livro",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "rows": 2,
                    "cols": 30,
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "language": forms.Select(
                attrs={
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                }
            ),
            "isbn": forms.TextInput(
                attrs={
                    "placeholder": "Digite o ISBN",
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "publisher": forms.Select(
                attrs={
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                }
            ),
            "categories": forms.SelectMultiple(
                attrs={
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                }
            ),
            "authors": forms.SelectMultiple(
                attrs={
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                }
            ),
            "publication_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "document": forms.ClearableFileInput(
                attrs={
                    "class": "w-full text-gray-400 text-sm bg-white border file:cursor-pointer cursor-pointer file:border-0 file:py-3 file:px-4 file:mr-4 file:bg-gray-100 file:hover:bg-gray-200 file:text-gray-800 rounded"
                }
            ),
            "pages": forms.NumberInput(
                attrs={
                    "placeholder": "Digite o número de páginas",
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "edition": forms.NumberInput(
                attrs={
                    "placeholder": "Digite a edição",
                    "class": "mt-1 block w-full text-gray-800 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500",
                }
            ),
        }
        labels = {
            "cover": "Capa do Livro",
            "title": "Título",
            "authors": "Autores",
            "summary": "Resumo",
            "isbn": "ISBN",
            "publisher": "Editora",
            "categories": "Categorias",
            "publication_date": "Data de Publicação",
            "document": "Arquivo do Livro",
            "language": "Idioma",
            "pages": "Número de Páginas",
            "edition": "Edição",
        }
        help_texts = {
            "edition": "Por padrão, o sistema registra como a primeira edição do livro, se não especificado.",
        }

    def clean_isbn(self):
        isbn = self.data.get("isbn")

        if len(isbn) != 13:
            raise forms.ValidationError("O ISBN deve ter 13 caracteres.")

        return isbn

    def clean_publication_date(self):
        publication_date = self.data.get("publication_date")

        if publication_date and publication_date > datetime.date.today():
            raise forms.ValidationError("A data de publicação não pode ser no futuro.")

        return publication_date

    def clean_edition(self):
        edition = self.data.get("edition")

        if edition is not None and edition <= 0:
            raise forms.ValidationError("A edição deve ser um número positivo.")

        return edition

    def clean_pages(self):
        pages = self.data.get("pages")
        if pages <= 0:
            raise forms.ValidationError("O número de páginas deve ser maior que 0.")
        return pages

class SugestionForm(forms.Form):
    about = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "formbold-form-input mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "placeholder": "Assunto",
                "id": "about",
                "name": "about",
            }
        )
    )

    sugestion = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "cols": 30,
                "class": "formbold-form-input mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "placeholder": "Sugestão",
                "id": "sugestion",
                "name": "sugestion",
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SugestionForm, self).clean()

        about = self.cleaned_data.get("about", "").strip()
        sugestion = self.cleaned_data.get("sugestion", "").strip() 

        if not about:
            raise forms.ValidationError(message="Campo (Sobre) não foi preechido!")
        
        if not sugestion:
            raise forms.ValidationError(message="Campo (sugestão) não foi preechido")

        return self.cleaned_data
    
    def save(self):
        """
        Save the Sugestion Form in the database Sugestion

        attr:
            - user: Is the Reader, mean the User loged
                * give it: request.user
        """
        self.clean()

        sugestion = Sugestion(
            user=self.request.user,
            about=self.cleaned_data['about'],
            text=self.cleaned_data['sugestion'],
            date_sugested=timezone.now()
        )

        sugestion.save()

