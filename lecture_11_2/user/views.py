from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from django.contrib.auth.models import auth
from django.contrib.auth import login
from .models import ResetPassword, Profile
from django import template
from django.core.mail import send_mail
from datetime import datetime, timezone
from django.contrib.auth.models import User
import uuid

RESET_PASSWORD_TOKEN_EXPIRATION_PERIOD = 2 * 60 * 60


def login_page_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.data.get('username'), password=form.data.get('password'))
            login(request, user)
            if user is not None:
                return redirect(to='index_page')
            else:
                form.add_error(field='username', error='Invalid password or login')
                return render(request, 'user/login.html', {'form': form})
        else:
            return render(request, 'user/login.html', {'form': form})


def register_page_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_data = auth.authenticate(request, username=user.username, email=user.email, password=form.data.get('password'))
            print(auth_data, form.errors)
            profile = Profile(owner_id=user.id)
            profile.save()
            if auth_data is not None:
                login(request, auth_data)
                return redirect(to='index_page')
        return render(request, 'user/register.html', {'form': form})


def handle_logout(request):
    auth.logout(request)
    return redirect('/auth/login')


def forgot_password_view(request):
    if request.method == 'GET':
        form = ForgotPasswordForm()
        return render(request, 'user/forgot-password.html', {'form': form})
    else:
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.data.get('email')
            token = uuid.uuid4()
            reset_password = ResetPassword(email=email, token=token)
            reset_password.save()
            email_template = template.loader.get_template('user/reset-password-mail.html')
            email_content = email_template.render(
                {'URL': 'http://localhost:8000/auth/reset-password',
                 'TOKEN': token})
            try:
                send_mail(subject='Reset Your Password', message='', html_message=email_content,
                          from_email='settings.EMAIL_HOST_USER', recipient_list=[email], fail_silently=False)
                return render(request, 'user/forgot-password.html', {'form': form, 'status': 'success'})
            except:
                return render(request, 'user/forgot-password.html', {'form': form, 'status': 'failed'})
        else:
            return render(request, 'user/forgot-password.html', {'form': form})


def reset_password_view(request, token):
    if request.method == 'GET':
        form = ResetPasswordForm()
        return render(request, 'user/reset-password.html', {'form': form})
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                reset_password = ResetPassword.objects.get(token=token)
                email = reset_password.email
                created_at = reset_password.created_at
                if (datetime.now(timezone.utc) - created_at).total_seconds() > RESET_PASSWORD_TOKEN_EXPIRATION_PERIOD:
                    reset_password.delete()
                    return render(request, 'user/reset-password.html',
                                  {'form': form, 'message': 'Your link is expired, please, try again!'})
                else:
                    user = User.objects.get(email=email)
                    user.set_password(form.data.get('password'))
                    user.save()
                    return render(request, 'user/reset-password.html', {'form': form, 'status': 'success'})
            except ResetPassword.DoesNotExist:
                return render(request, 'user/reset-password.html',
                                  {'form': form, 'message': 'No data found, try again!'})
        else:
            return render(request, 'user/reset-password.html', {'form': form})




def settings_page_view(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/auth/login/')

    profile = Profile.objects.get(owner_id=request.user.id)

    if request.method == 'GET':
        form = ProfileForm(data={'bio': profile.bio}, files={'avatar': profile.avatar, 'resume': profile.resume})
        return render(request, 'user/settings.html', {'form': form, 'profile': profile})
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            if form.files.get('avatar'):
                profile.avatar = form.files.get('avatar')
            if form.files.get('resume'):
                profile.resume = form.files.get('resume')
            profile.bio = form.data.get('bio')
            profile.save()
            return render(request, 'user/settings.html', {'form': form, 'profile': profile})
        else:
            return render(request, 'user/settings.html', {'form': form, 'profile': profile})


