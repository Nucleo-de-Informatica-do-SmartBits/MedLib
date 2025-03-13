import json
import secrets

from django.contrib import messages
from django.contrib.auth import login, get_user
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse

from .forms import ReaderAuthenticationForm, ReaderCreationForm
from .models import Reader

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


@login_required
def profile(request):
    user = get_user(request)
    user.reader, _ = Reader.objects.get_or_create(user=user)

    if request.method == "POST":
        data = request.POST.dict()
        photo = request.FILES.get('photo', None)
        
        if photo:
            user.reader.photo.save(photo.name, photo)

        if not data:
            messages.error(request, "Os dados enviados não são válidos.")
            return JsonResponse({"error": "Invalid form data"}, status=400)
        
        new_password = data.pop("new_password", None)

        if new_password:
            actual_password = data.pop("actual_password", None)

            if not secrets.compare_digest(actual_password, new_password):
                if new_password and not actual_password:
                    messages.error(request, "A palavra-passe atual é obrigatória.")
                    return JsonResponse(
                        {"error": "A palavra-passe atual é obrigatória."}, status=400
                    )

                if not user.check_password(actual_password):
                    messages.error(request, "Palavras-passe actual incorrecta.")
                    return JsonResponse(
                        {"error": "Palavras-passe actual incorrecta."}, status=400
                    )

                user.set_password(new_password)

        email = data.pop("email", None)

        if email and email != user.email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Email inválido.")
                return JsonResponse({"error": "Invalid email format"}, status=400)
            user.email = email
        
        for k, v in data.items():
            if v and getattr(user, k, None) != v:
                setattr(user, k, v)
            elif v and hasattr(user.reader, k):
                setattr(user.reader, k, v)
            
        if new_password  or email or data or photo:
            user.save()

        messages.success(request, "Dados atualizados com sucesso.")
        return JsonResponse({"success": "Data received"}, status=200)

        

  

    return render(request, "control/profile.html")

