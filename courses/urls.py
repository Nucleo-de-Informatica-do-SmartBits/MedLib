from django.urls import path
from courses.views import (
    list_courses,
    view_course,
    get_video_data,
    filter_courses
)

urlpatterns = [
    path("", list_courses, name="courses"),
    path("view-course/<course_slug>/<course_uuid>/", view_course, name="view_course"),
    path("get-video-data/<video_slug>/<video_uuid>/", get_video_data, name="get_video_data"),
    path("filter/", filter_courses, name="filter_courses"),
]
