from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка Django по адресу /superadmin/
    path('superadmin/', admin.site.urls),
    
    # Подключаем маршруты нашего приложения portal
    path('', include('portal.urls')),
]

# Настройка для отображения медиа-файлов (фото) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)