from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404, handler500, static

import blog.views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path("python-tutorial/", include('python.urls')),
    path('java-tutorial/', include('java.urls')),

    # summernote
    path('summernote/', include('django_summernote.urls')),

    # api
    path("api/blog/", include('blog.api.urls')),
]
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = blog_views.handler404
# handler500 = blog.views.handler500
