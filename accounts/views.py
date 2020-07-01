import logging
import math
from random import random

from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect

# Create your views here.
from .forms import LoginForm, RegistrationForm, RegistrationForm2, PhoneForm, LoginForm2
from .models import User


def get_otp():
    nums = "0123456789"
    OTP_CODE = ""
    res = [i for i in range(4)]
    for i in range(4):
        OTP_CODE += nums[math.floor(random() * 10)]
    return OTP_CODE


def get_registration_form(phone_number):
    user = User.objects.filter(phone_number__iexact=phone_number).first()
    if bool(not user and not User.objects.all()):
        form = RegistrationForm
    else:
        form = RegistrationForm2
    return form


def send_phone_number(request):
    ''' Checking if a user exists by phone number in User model and return a view for login or registration '''

    code = get_otp()
    print('otp = ', code)
    logging.basicConfig(filename="auth.log", level=logging.INFO)
    logging.info(code)
    request.session['otp'] = code
    if request.method == 'POST':
        form = PhoneForm(request.POST)

        if form.is_valid():
            user = User.objects.filter(phone_number=form.cleaned_data.get('phone_number')).first()
            request.session['phone_number'] = form.cleaned_data.get('phone_number')

            if user:  # if user exist
                return redirect(reverse('accounts:LoginView_url'))
            else:  # if User does not exist
                return redirect(reverse('accounts:RegistrationView_url'))
    else:
        form = PhoneForm()

    return render(request, 'signup_init.html', {'form': form})


def profile_account(request):
    user = request.user
    return render(request, 'profile.html', context={'user': user})


class RegistrationView(View):
    model = User
    template = 'registration.html'

    def get(self, request):
        phone = request.session['phone_number']
        form = get_registration_form(phone)
        return render(request, self.template, context={'form': form})

    def post(self, request):
        phone = request.session['phone_number']
        form = get_registration_form(phone)

        bound_form = form(request.POST)

        if bound_form.is_valid():
            if bound_form.cleaned_data.get('otp_code') == request.session['otp']:
                if not User.objects.all():
                    user = bound_form.save()
                    user.refresh_from_db()
                    user.first_name = bound_form.cleaned_data.get('first_name')
                    user.last_name = bound_form.cleaned_data.get('last_name')
                    user.password = bound_form.cleaned_data.get('password1')
                    user.is_employee = True
                    user.phone_number = request.session['phone_number']
                    user.save()
                    user = login(request, user)
                    return redirect(reverse('accounts:profile_account_url'))
                else:
                    first_name = bound_form.cleaned_data["first_name"]
                    last_name = bound_form.cleaned_data["last_name"]
                    user = User.objects.create(first_name=first_name, last_name=last_name, phone_number=phone)
                    user = login(request, user)

                    return redirect(reverse('accounts:profile_account_url'))
            else:
                raise ValueError('Wrong otp code!')
        else:
            return render(request, self.template, context={'form': bound_form})


class LoginView(View):
    model = User
    template = 'login.html'

    def get(self, request):
        phone = request.session['phone_number']
        user = User.objects.filter(phone_number=phone).first()
        if user.is_employee:
            form = LoginForm
        else:
            form = LoginForm2
        return render(request, self.template, context={'form': form})

    def post(self, request):
        phone = request.session['phone_number']
        user = User.objects.filter(phone_number=phone).first()
        if user.is_employee:
            form = LoginForm
        else:
            form = LoginForm2
        bound_form = form(request.POST)
        if bound_form.is_valid():
            if bound_form.cleaned_data.get('otp_code') == request.session['otp']:
                if bound_form.prefix == 'LoginForm2':
                    user = login(request, user)
                    return render(request, 'profile.html')
                elif bound_form.cleaned_data.get('password') == user.password:
                    user = login(request, user)
                    return render(request, 'profile.html')
                else:
                    return HttpResponse("Вы указали неверный пароль.")
            else:
                raise ValueError('Wrong otp code!')
