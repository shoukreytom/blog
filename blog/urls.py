from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    re_path(r'^404', views.handler404),
    path('', views.PostsList.as_view(), name="blog-home"),
    path('post/<int:pk>/', views.PostDetail.as_view(), name="post-detail"),
    path('about/', views.about, name="about"),
    path('contact/', views.ContactView.as_view(), name="contact")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
