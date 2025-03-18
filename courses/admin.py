from django.contrib import admin
from courses.models import Course, Video, Faq

admin.site.register((Course, Video, Faq))
