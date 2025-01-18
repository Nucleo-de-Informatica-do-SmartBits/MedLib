from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def courses(request):
      template_name = "courses/course.html"
      ctx = {}

      return render(request=request, template_name=template_name, context=ctx)