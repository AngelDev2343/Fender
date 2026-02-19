# (urls.py del PROYECTO)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importar
from django.conf.urls.static import static # Importar

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conecta todas las URLs de tu app 'app_fender'
    path('', include('app_fender.urls')), 
]

# Esto es necesario para ver las imágenes que subas (ej. de productos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)