from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.utils import IntegrityError

from accounts.models import Account


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        if username and email and password1:
            if password1 == password2:
                try:
                    account = Account.objects.create(username=username, email=email)
                    account.set_password(password1)
                    account.save()
                    return redirect('signin')
                except IntegrityError:
                    messages.error(request, "username or email is already exists.")
            else:
                messages.error(request, "passwords don't match")
        else:
            messages.error(request, "please provide valid data for all fields.")
    return render(request, 'accounts/signup.html')

@csrf_exempt
def signin(request):
    if request.user.is_authenticated:
        messages.error(request, "you're already logged in.")
        return redirect('blog-home')
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user=user)
                return redirect('blog-home')
            else:
                messages.error(request, "email or password is incorrect")
        else:
            messages.error(request, "please fill all fields with a valid data")
    return render(request, 'accounts/signin.html')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('blog-home')
    else:
        messages.error(request, "you're not logged in. please login instead.")
        return redirect('signin')

def profile(request):
    pass
