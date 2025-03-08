from django.urls import path
from courses.views import (
    list_courses,
    view_course,
    watch_video,
    filter_courses
)

urlpatterns = [
    path("", list_courses, name="courses"),
    path("view-course/<course_slug>/<course_uuid>/", view_course, name="view_course"),
    path("watch/<slug:video_slug>/", watch_video, name="watch_video"),
    path("filter/", filter_courses, name="filter_courses"),
]
