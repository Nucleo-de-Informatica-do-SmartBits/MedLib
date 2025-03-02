from django.urls import path
from courses.views import access_courses, access_courses_video, access_courses_video_watch

urlpatterns = [
    path(route="", view=access_courses, name="courses"),
    path(route="courses_video/<slug:slug>/", view=access_courses_video, name="courses_video"),
    path(route="courses_watch/<slug:video>/", view=access_courses_video_watch, name="courses_watch"),
]
