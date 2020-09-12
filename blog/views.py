from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.defaults import page_not_found

from .models import Post
from .forms import ContactForm


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
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid:
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			message = form.cleaned_data['message']
			#TODO: send message to the author
			return redirect('blog-home')
	form = ContactForm()
	return render(request, "blog/contact.html", {'form': form})


def handler404(request, exception):
	return page_not_found(request, exception, template_name="blog/404.html")
