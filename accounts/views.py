from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.utils import IntegrityError

from accounts.models import Account


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        if username and email and password1 and (password1 == password2):
            try:
                account = Account.objects.create(username=username, email=email)
                account.set_password(password1)
                account.save()
                return redirect('signin')
            except IntegrityError:
                messages.error(request, "username or email is already exists.")
        else:
            messages.error(request, "please provide valid data for all fields.")
    return render(request, 'accounts/signup.html')

def signin(request):
    return render(request, 'accounts/signin.html')

def signout(request):
    pass

def profile(request):
    pass
