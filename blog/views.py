from django.shortcuts import render
from django.views.generic import ListView, DetailView

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
