from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm,OTPVerificationForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile
from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator
from .models import Profile

from django.urls import resolve
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout as auth_logout



from django.core.mail import send_mail

from .models import OTP
from .forms import OTPVerificationForm
from django.utils import timezone
from datetime import timedelta

def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('index')
	else:

		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)

def Signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:landing')
        else:
            return render(request, 'signin.html', {'error': 'Invalid username or password'})
    return render(request, 'signin.html')


@login_required
def profile_view(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('authy:signin')


def generate_otp(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'requestotp.html', {'error': 'User does not exist'})
        
        otp = OTP.objects.create(user=user)
        otp.generate_otp_code()
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'adityauttaravilli@gmail.com',  # Replace with your email
            [user.email],
            fail_silently=False,
        )
        return redirect('verify_otp')
    
    return render(request, 'requestotp.html')

def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            try:
                otp = OTP.objects.get(otp_code=otp_code, is_verified=False)
                if timezone.now() - otp.created_at < timedelta(minutes=10):  # OTP validity
                    otp.is_verified = True
                    otp.save()
                    return redirect('password_change')
                else:
                    return render(request, 'verifyotp.html', {'form': form, 'error': 'OTP has expired'})
            except OTP.DoesNotExist:
                return render(request, 'verifyotp.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        form = OTPVerificationForm()
    
    return render(request, 'verifyotp.html', {'form': form})

def password_change(request):
    if request.method == 'POST':
        # Handle password change logic
        pass
    return render(request, 'changepassword.html')