from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

import blog.views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path("python-tutorial/", include('python.urls')),
    path('java-tutorial/', include('java.urls')),

    # summernote
    path('summernote/', include('django_summernote')),

    # api
    path("api/blog/", include('blog.api.urls')),
]

handler404 = blog_views.handler404
# handler500 = blog.views.handler500
