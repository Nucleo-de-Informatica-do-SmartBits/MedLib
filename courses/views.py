from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from courses.models import Course, Video, Faq


def list_courses(request):
    template_name = "courses/courses-list.html"
    courses = Course.objects.all()
    return render(request, template_name, {"courses": courses})


def view_course(request, course_slug, course_uuid):
    template_name = "courses/courses-video.html"
    
    course = get_object_or_404(Course, slug=course_slug, uuid=course_uuid)
    videos = Video.objects.filter(course=course)
    faq_list = Faq.objects.filter(course=course)

    context = {
        "videos": videos,
        "course": course,
        "faq_list": faq_list,
        "total_videos": course.get_total_videos,
        "total_duration": course.get_total_videos_duration
    }
    return render(request, template_name, context)

            ctx["courses"] = courses

      return render(request=request, template_name=template_name, context=ctx)

@login_required
def get_video_data(request, video_slug, video_uuid):
    video = get_object_or_404(Video, slug=video_slug, uuid=video_uuid)

    return JsonResponse({
        'title':video.title,
        'video_path': video.video.url,
        'video_cover_path': video.cover.url
    })

      return render(request=request, template_name=tn, context=ctx)

<<<<<<< HEAD
@login_required
def access_courses_video_watch(request, video):
      tn = "courses/courses-watch.html"
      ctx = {}

      video_main: Video = Video.objects.get(slug=video)
      course = video_main.curso
      course: Video = Video.objects.filter(curso=course)

      pg = Paginator(course, 2)

      if request.method == "GET":
            page_numer = request.GET.get("page")

            pg = pg.get_page(page_numer)
                  
            ctx["video_main"] = video_main
            ctx["course"] = course
            ctx["paginator"] = pg

            return render(request=request, template_name=tn, context=ctx)
=======
def filter_courses(request):
    category = request.GET.get("category", "ALL")

    if category == "ALL":
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(category=category)

    return render(request, "partials/courses_list.html", {"courses": courses})
>>>>>>> dev
