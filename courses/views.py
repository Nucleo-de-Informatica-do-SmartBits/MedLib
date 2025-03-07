from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course, Video
from django.core.paginator import Paginator


# Create your views here.
@login_required
def access_courses(request):
    template_name = "courses/courses-list.html"
    courses: Course = Course.objects.all()

    return render(
        request=request, template_name=template_name, context={"courses": courses}
    )


@login_required
def access_courses_video(request, slug):
    tn = "courses/courses-video.html"
    ctx = {}

    # get all video in courses that have this slug
    course: Course = Course.objects.get(slug=slug)
    videos: Video = Video.objects.filter(course=course)

    ctx["videos"] = videos
    ctx["course"] = course

    return render(request=request, template_name=tn, context=ctx)


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
