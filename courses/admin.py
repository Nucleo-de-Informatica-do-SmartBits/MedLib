from django.contrib import admin
from courses.models import Teacher, Course, Video, Comment

# Register your models here.
admin.site.register((Teacher, Course, Video, Comment))