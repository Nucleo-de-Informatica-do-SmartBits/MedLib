from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ReaderAuthenticationForm, ReaderCreationForm


def just_not_authenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Você já está logado!")
            return redirect(reverse("home"))

        return func(request, *args, **kwargs)

    return wrapper


@just_not_authenticated_user
def signup(request):
    ctx = {}
    template_name = "control/signup.html"

    if request.method == "POST":
        form = ReaderCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Dados registrados com sucesso!")
            return redirect(reverse("signin"))
    else:
        form = ReaderCreationForm()

    ctx["form"] = form
    return render(request, template_name, ctx)


@just_not_authenticated_user
def signin(request):
    ctx = {}
    template_name = "control/signin.html"

    if request.method == "POST":
        form = ReaderAuthenticationForm(data=request.POST, request=request)

        if form.is_valid():
            user = form.get_user()

            if user is not None:
                login(request, user)

                messages.success(request, "Sessão iniciada com sucesso!")
                return redirect(reverse("home"))
    else:
        form = ReaderAuthenticationForm()

    ctx["form"] = form
    return render(request, template_name, ctx)


@login_required
def logout(request):
    auth_logout(request)

    messages.info(request, "Sessão fechado com sucesso!")
    return redirect(reverse("signin"))
