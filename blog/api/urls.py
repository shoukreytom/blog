from django.urls import path

from blog.api.views import post_detail_view


app_name = "blog"


urlpatterns = [
    path("<int:pk>/", post_detail_view, name="detail"),
]
