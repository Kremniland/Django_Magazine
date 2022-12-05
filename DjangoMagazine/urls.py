from django.contrib import admin
from django.urls import path, include
# Pillow (картинки)
from django.conf import settings
from django.conf.urls.static import static

from django.views.defaults import ERROR_400_TEMPLATE_NAME

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
    path('basket/', include('basket.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400
# handler403
handler404 = 'book.views.error_404'
# handler500