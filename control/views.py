from django.shortcuts import render, redirect
from .models import Reader, User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse


def signup(request):
    done: str = str(request.GET.get('done')) == "0" # Can change if an tailwind alert

    ctx = {'done': done}
    template_name = "control/signup.html"

    if request.method == "POST":
        firstname: str = request.POST.get('firstname')
        lastname: str = request.POST.get('lastname')
        process_number: int = request.POST.get('num-process')
        course: str = request.POST.get('course')
        grade: int = request.POST.get('grade')
        group: str = request.POST.get('group')
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')
        confirm_password: str = request.POST.get('confirm-password')
        profile_photo: str = request.FILES.get('upload')

        if not reader_authenticate(password, confirm_password, process_number):
            return redirect('/auth/signup?done=0')
        
        user: User = User.objects.create_user(
            username=firstname+lastname, 
            email=email, password=password, 
            first_name=firstname, 
            last_name=lastname
        )
        user.save()

        reader: Reader = Reader.objects.create(
            user=user,
            process_number=process_number,
            grade=grade,
            course=course,
            group=group,
            photo=profile_photo
        )
        reader.save()

        return redirect('signin')

    return render(request, template_name, ctx)


def signin(request):
    ctx = {}
    template_name = "control/signin.html"

    if request.method == "POST":
        process_number: int = request.POST.get('num-process')
        password: str = request.POST.get('password')

        if Reader.objects.filter(process_number=process_number).exists() == False:
            return redirect('/auth/signin?done=0')
        
        reader: Reader = Reader.objects.get(process_number=process_number)
        user = authenticate(request, username=reader.user.username, password=password)
        if user is not None:
            login(request=request, user=user)
            return HttpResponse(f'{user.username}-----{user.password}')        

    return render(request, template_name, ctx)


def reader_authenticate( password: str, confirm_password: str, process_number: int ) -> bool:
    is_process_number: bool =  Reader.objects.filter(process_number=process_number).exists()
    return (password == confirm_password) and (is_process_number == False)