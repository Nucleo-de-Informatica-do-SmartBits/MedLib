from django.contrib import admin
from courses.models import Course, Video

admin.site.register((Course, Video))
