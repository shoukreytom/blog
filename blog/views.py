from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.defaults import page_not_found
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from .models import Post
from .forms import CreatePostForm, ContactForm


class PostsList(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginated_by = 15
    ordering = ['-publish']

    def get_queryset(self):
        return Post.published.values()


class PostDetail(DetailView):
    model = Post

class CreatePost(CreateView):
    empty_form = CreatePostForm()
    def get(self, request, *args, **kwargs):
        ctx = {
            'form': self.empty_form,
        }
        return render(request, "blog/create_post.html", ctx)
    
    def post(self, request, *args, **kwargs):
        filled_form = CreatePostForm(request.POST)
        if filled_form.is_valid():
            post = filled_form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been added successfully.")
            return redirect('blog-home')
        else:
            messages.error(request, "please make sure that you've filled all field with a valid data.")
        ctx = {
            'form': self.empty_form,
        }
        return render(request, "blog/create_post.html")


def about(request):
    return render(request, "blog/about.html")


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {"form": form}
        return render(request, "blog/contact.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            send_mail('sttech feedback ({})'.format(name), message, email,
                      [settings.EMAIL_HOST_USER, ], fail_silently=False)
            return redirect('blog-home')
        return redirect(request.path)


def handler404(request, exception):
    return page_not_found(request, exception, template_name="errors/404.html")
