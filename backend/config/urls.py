from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'),name='base'), #for demo purpose :D
    path('admin/', admin.site.urls),

    # api
    path('api/v1/', include('api.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
