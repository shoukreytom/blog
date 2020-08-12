from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.defaults import page_not_found

from .models import Post


class PostsList(ListView):
	model = Post
	template_name = "blog/index.html"
	context_object_name = "posts"
	paginated_by = 15
	ordering = ['-date_posted']


class PostDetail(DetailView):
	model = Post	


def about(request):
	return render(request, "blog/about.html")

def contact(request):
	return render(request, "blog/contact.html")


def handler404(request, exception):
	return page_not_found(request, exception, template_name="blog/404.html")
