from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    path("library/", include("library.urls")),
    path("courses/", include("courses.urls")),
    path("auth/", include("control.urls")),
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url=reverse_lazy('home'))) 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)