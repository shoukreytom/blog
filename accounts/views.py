from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.core.mail import message, send_mail
from django.contrib.auth import login, authenticate, logout
from django.db.utils import IntegrityError
import secrets

from accounts.models import Account, Token


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
                    if send_confirmation_url(request, email, username):
                        messages.success(request, "please check your email, we've sent a message with confirmation url to you.")
                    return redirect('signin')
                except IntegrityError:
                    messages.error(request, "username or email is already exists.", 'danger')
            else:
                messages.error(request, "passwords don't match", 'danger')
        else:
            messages.error(request, "please provide valid data for all fields.", 'danger')
    return render(request, 'accounts/signup.html')

@csrf_exempt
def signin(request):
    if request.user.is_authenticated:
        messages.error(request, "you're already logged in.", 'danger')
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
                messages.error(request, "email or password is incorrect", 'danger')
        else:
            messages.error(request, "please fill all fields with a valid data", 'danger')
    return render(request, 'accounts/signin.html')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('blog-home')
    else:
        messages.error(request, "you're not logged in. please login instead.", 'danger')
        return redirect('signin')

def profile(request):
    return render(request, 'accounts/profile.html')

def confirm_email(request, token):
    if request.method == 'POST':
        generate_token()
    else:
        try:
            token = Token.objects.get(token=token)
            user = token.user
            user.is_verified = True
            user.save()
            messages.success(request, "You've confirmed you eamil successfully.")
            return redirect('blog-home')
        except Token.DoesNotExist:
            messages.error(request, "Invalid confirmation url.", 'danger')
            return redirect('blog-home')
    return render(request, 'accounts/confirm_email.html')

# Helper methods
def send_confirmation_url(request, email, username):
    host = "https://"+str(request.get_host())
    path = "/accounts/email/confirm/"
    token = generate_token()
    url = host + path + token + "/"
    message = "Hi {username}, Thank you for joining us, please click this link: {url} to confirm your email.".format(username=username, url=url)
    try:
        send_mail("Confirm Email", message, settings.EMAIL_HOST_USER, [email, ])
        user = Account.objects.get(username=username)
        token_obj = Token.objects.create(token=token, user=user)
        token_obj.save()
    except:
        return False
    return True

def generate_token():
    token = secrets.token_hex(39)
    return token 
