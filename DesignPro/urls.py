from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Административная панель по адресу /superadmin/ (как в ТЗ)
    path('superadmin/', admin.site.urls),

    # Подключаем маршруты нашего приложения portal
    path('', include('portal.urls')),
]

# Настройка для отображения загруженных медиа-файлов (фото, дизайн) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)