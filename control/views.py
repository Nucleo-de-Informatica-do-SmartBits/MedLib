from django.shortcuts import render, redirect
from .models import Reader, User


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
        group: int = request.POST.get('group')
        email: int = request.POST.get('email')
        password: int = request.POST.get('password')
        confirm_password: int = request.POST.get('confirm-password')
        profile_photo: int = request.FILES.get('upload')

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
        ...

    return render(request, template_name, ctx)


def reader_authenticate( password: str, confirm_password: str, process_number: int ) -> bool:
    is_process_number: bool =  Reader.objects.filter(process_number=process_number).exists()
    print(is_process_number)
    return (password == confirm_password) and (is_process_number == False)