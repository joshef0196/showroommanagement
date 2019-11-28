
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('',include('showroom.urls')),
    path('/',include('showroom.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
