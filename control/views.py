from django.shortcuts import render


def signup(request): 
    ctx = {}
    template_name = "control/signup.html"


    if request.method == "POST":
        ...
    
    return render(request, template_name, ctx)