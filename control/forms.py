import unicodedata
from secrets import compare_digest

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Reader


class ReaderCreationForm(forms.Form):
    firstname = forms.CharField(
        label="Primeiro Nomee",
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "formbold-form-input", "placeholder": "Primeiro nome"}
        ),
    )

    lastname = forms.CharField(
        label="Sobrenome",
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "formbold-form-input", "placeholder": "Sobrenome"}
        ),
    )

    process_number = forms.CharField(
        label="Número de processo",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "formbold-form-input",
                "placeholder": "Número de processo, exemplo: 1234",
                "id": "num-process",
            }
        ),
    )

    course = forms.ChoiceField(
        label="Curso",
        choices=[
            ("Informática", "Informática"),
            ("Eletrónica", "Eletrónica"),
        ],
        widget=forms.Select(
            attrs={
                "class": "formbold-form-input",
                "id": "occupation",
                "required": "",
            }
        ),
    )

    grade = forms.ChoiceField(
        label="Classe",
        choices=[
            ("10", "Décima"),
            ("11", "Décima Primeira"),
            ("12", "Décima Segunda"),
            ("13", "Décima Terceira"),
        ],
        widget=forms.Select(
            attrs={
                "class": "formbold-form-input",
                "id": "occupation",
                "required": "",
            }
        ),
    )

    group = forms.ChoiceField(
        label="Turma",
        choices=[
            ("A", "Turma A"),
            ("B", "Turma B"),
            ("C", "Turma C"),
            ("D", "Turma D"),
        ],
        widget=forms.RadioSelect(attrs={"class": "turma-option"}),
        required=True,
    )

    password = forms.CharField(
        label="Palavra-passe",
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "formbold-form-input",
                "minlength": 8,
                "required": "",
                "placeholder": "Palavra-passe",
            }
        ),
    )

    confirm_password = forms.CharField(
        label="Confirmar Palavra-passe",
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "formbold-form-input",
                "minlength": 8,
                "required": "",
                "placeholder": "Confirmar Palavra-passe",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].choices.insert(0, ("", "Selecione o seu curso"))
        self.fields["grade"].choices.insert(0, ("", "Selecione a sua classe"))

    def clean(self):
        cleaned_data = super().clean()

        firstname = cleaned_data.get("firstname", "").strip()
        lastname = cleaned_data.get("lastname", "").strip()
        process_number = cleaned_data.get("process_number", "").strip()
        course = cleaned_data.get("course", "").strip()
        grade = cleaned_data.get("grade", "").strip()
        group = cleaned_data.get("group", "").strip()
        password = cleaned_data.get("password", "").strip()
        confirm_password = cleaned_data.get("confirm_password", "").strip()

        if not firstname:
            raise forms.ValidationError("Preencha o campo, por favor!")

        if not lastname:
            raise forms.ValidationError("Preencha o campo, por favor!")

        if not process_number.isdigit():
            raise forms.ValidationError(
                "Número de processo deve conter apenas dígitos!"
            )

        if Reader.objects.filter(process_number=process_number).exists():
            raise forms.ValidationError("Número de processo já registrado!")

        if course not in ("Informática", "Electrónica"):
            raise forms.ValidationError("Este curso não está disponível!")

        if grade not in ("10", "11", "12", "13"):
            raise forms.ValidationError("Classe inválida!")

        if group not in ("A", "B", "C", "D"):
            raise forms.ValidationError("Turma inválida")

        if not password:
            raise forms.ValidationError("Por favor, digite a palavra-passe!")

        elif len(password) < 8:
            raise forms.ValidationError(
                "A palavra-passe deve ter pelo menos 8 caracteres!"
            )

        if not confirm_password:
            raise forms.ValidationError("Por favor, confirme a palavra-passe!")

        elif not compare_digest(password, confirm_password):
            raise forms.ValidationError("As palavras-passe não coincidem!")

        return cleaned_data

    def create_username(self, firstname, lastname):
        _base_username = unicodedata.normalize(
            "NFKD", f"{firstname}-{lastname}".lower()
        )
        base_username = "".join(
            [c for c in _base_username if not unicodedata.combining(c)]
        )

        count = User.objects.filter(username__startswith=base_username).count()
        return f"{base_username}-{count + 1}" if count else base_username

    def save(self):
        data = super().clean()

        user = User.objects.create_user(
            username=self.create_username(
                firstname=data.get("firstname"), lastname=data.get("lastname")
            ),
            first_name=data.get("firstname"),
            last_name=data.get("lastname"),
            password=data.get("password"),
        )

        reader = Reader.objects.create(
            user=user,
            process_number=data.get("process_number"),
            course=data.get("course"),
            grade=data.get("grade"),
            group=data.get("group"),
        )

        reader.save()


class ReaderAuthenticationForm(forms.Form):
    process_number = forms.CharField(
        label="Número de processo",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "formbold-form-input mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "placeholder": "Número de processo",
                "id": "num-process",
            }
        ),
    )

    password = forms.CharField(
        label="Palavra-passe",
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "formbold-form-input mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                "minlength": 8,
                "placeholder": "Palavra-passe",
                "id": "password",
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        process_number = cleaned_data.get("process_number", "").strip()
        password = cleaned_data.get("password", "").strip()

        if not process_number or not password:
            raise forms.ValidationError("Por favor, preencha todos os campos!")

        if (not process_number.isdigit()) or int(process_number) < 0:
            raise forms.ValidationError("Número de processo inválido.")

        reader = Reader.objects.filter(process_number=process_number).first()

        if not reader:
            raise forms.ValidationError("Número de processo inválido")
        else:
            self.user = authenticate(
                self.request, username=reader.user.username, password=password
            )

            if not self.user:
                raise forms.ValidationError(
                    "Número de processo ou Palavra-passe incorrectos"
                )

        return cleaned_data

    def get_user(self):
        return self.user
