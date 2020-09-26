from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.views.defaults import page_not_found
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

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
    return page_not_found(request, exception, template_name="blog/404.html")
