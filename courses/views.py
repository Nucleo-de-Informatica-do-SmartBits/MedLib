from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course, Teacher, Video

# Create your views here.
@login_required
def access_courses(request):
      template_name = "courses/courses-list.html"
      ctx = {}

      if request.method == "GET":
            courses: Course = Course.objects.all()
            ctx.update({"courses": courses})

      return render(request=request, template_name=template_name, context=ctx)

@login_required
def access_courses_video(request, slug):
      tn = "courses/courses-video.html"
      ctx = {}

      #get all video in courses that have this slug
      course: Course = Course.objects.get(slug=slug)
      videos: Video = Video.objects.filter(curso=course)

      ctx.update({"videos": videos})

      return render(request=request, template_name=tn, context=ctx)
      ...

@login_required
def access_courses_video_watch(request, slug):
      ...