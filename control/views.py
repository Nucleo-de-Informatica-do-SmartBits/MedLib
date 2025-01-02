import unicodedata
from secrets import compare_digest

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Reader, User


def just_not_authenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Você já está logado!")
            return redirect(reverse("home"))
        
        return func(request, *args, **kwargs)

    return wrapper


def validate_form(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    process_number = request.POST.get("num-process")
    course = request.POST.get("course")
    grade = request.POST.get("grade")
    group = request.POST.get("group")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm-password")

    if not compare_digest(password, confirm_password):
        messages.warning(request, "As palavras-passe não coincidem!")
        return False

    elif len(firstname.strip()) == 0 or len(lastname.strip()) == 0:
        messages.error(request, "Preencha todos os campos, por favor!")
        return False

    elif (
        process_number.isdigit()
        or Reader.objects.filter(process_number=process_number).exists()
    ):
        messages.error(request, "Número de processo inválido ou já registrado")
        return False

    elif course not in ("Informática", "Electrónica"):
        messages.error(request, "Este curso não está disponível!")
        return False

    elif grade not in ("10", "11", "12", "13"):
        messages.error(request, "Classe inválida!")
        return False

    elif group not in ("A", "B", "C", "D"):
        messages.error(request, "Turma inválida")
        return False

    return True


def create_username(firstname, lastname):
    _base_username = unicodedata.normalize("NFKD", f"{firstname}-{lastname}".lower())
    base_username = "".join([c for c in _base_username if not unicodedata.combining(c)])

    count = User.objects.filter(username__startswith=base_username).count()
    return f"{base_username}-{count + 1}" if count else base_username


@just_not_authenticated_user
def signup(request):
    template_name = "control/signup.html"

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        process_number = request.POST.get("num-process")
        course = request.POST.get("course")
        grade = request.POST.get("grade")
        group = request.POST.get("group")
        password = request.POST.get("password")

        if validate_form(request):
            user = User.objects.create_user(
                username=create_username(firstname=firstname, lastname=lastname),
                first_name=firstname,
                last_name=lastname,
                password=password,
            )

            reader = Reader.objects.create(
                user=user,
                process_number=process_number,
                grade=grade,
                course=course,
                group=group,
            )
            reader.save()

            messages.success(request, "Os seus dados foram registrados!")
            return redirect("signin")

        return redirect(reverse("signup"))
    return render(request, template_name)


@just_not_authenticated_user
def signin(request):
    template_name = "control/signin.html"

    if request.method == "POST":
        process_number = request.POST.get("num-process")
        password = request.POST.get("password")

        if not process_number.strip() or not password.strip():
            messages.error(request, "Por favor, preencha todos os campos1")
            return redirect(reverse("signin"))

        if not process_number.isdigit() or int(process_number) < 0:
            messages.error(request, "Número de processo inválido.")
            return redirect(reverse("signin"))

        reader = get_object_or_404(Reader, process_number=process_number)
        user = authenticate(request, username=reader.user.username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "Sessão iniciada com sucesso!")
            return redirect(reverse("home"))

        messages.warning(request, "Username ou Palavra-passe incorrectos!")
        return redirect(reverse("signin"))

    return render(request, template_name)


@login_required
def logout(request):
    auth_logout(request)

    messages.info(request, "Sessão fechado com sucesso!")
    return redirect(reverse("signin"))