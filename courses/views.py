from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from courses.models import Course, Video


@login_required
def list_courses(request):
    template_name = "courses/courses-list.html"
    courses = Course.objects.all()
    return render(request, template_name, {"courses": courses})


@login_required
def view_course(request, course_slug, course_uuid):
    template_name = "courses/courses-video.html"
    
    course = get_object_or_404(Course, slug=course_slug, uuid=course_uuid)
    videos = Video.objects.filter(curso=course)

    context = {
        "videos": videos,
        "course": course,
    }
    return render(request, template_name, context)


@login_required
def watch_video(request, video_slug):
    template_name = "courses/courses-watch.html"

    main_video = get_object_or_404(Video, slug=video_slug)
    related_videos = Video.objects.filter(curso=main_video.curso)

    paginator = Paginator(related_videos, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "video_main": main_video,
        "course": main_video.curso,
        "paginator": page_obj,
    }
    return render(request, template_name, context)


@login_required
def filter_courses(request):
    category = request.GET.get("category", "ALL")

    if category == "ALL":
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(category=category)

    return render(request, "partials/courses_list.html", {"courses": courses})
