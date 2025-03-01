from django.contrib import admin
from courses.models import Teacher, Course, Video

# Register your models here.
admin.site.register((Teacher, Course, Video))