from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from accounts.models import UserProfile


def login(request):
    if request.method == 'POST':
        # Login user
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(
            username=username,
            password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'pages/auth/login.html')


def reset_password(request):
    return render(request, 'pages/auth/reset-password.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('login')


def profile(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        print('User: {}'.format(user.username))

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        if user.username != username and User.objects.filter(username=username).exists():
            messages.error(request, 'That username is taken')
            return redirect('profile', username=username)
        else:
            if user.email != email and User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used')
                return redirect('profile', username=username)
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=username)
    else:
        return render(request, 'pages/profile/user_profile.html')


def update_image(request):
    if request.method == "POST":
        try:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            file = request.FILES['selected-file']
            user_profile.profile_picture = file
            user_profile.save()
            messages.success(request, 'Profile picture has been updated!')
            return redirect('profile', username=request.user.username)
        except MultiValueDictKeyError:
            print("No file selected")
            return redirect('profile', username=request.user.username)
    else:
        return render(request, 'pages/profile/user_profile.html')


