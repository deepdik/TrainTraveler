from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from apps.stations.models import Station
from apps.train_class.models import TrainClass
from apps.users.forms import LoginForm, SignupForm, UserProfileForm

# Create your views here.

User = get_user_model()


class HomeView(View):
    def get(self, request):
        # Get relevant data from the database
        stations = Station.objects.all()
        classes = TrainClass.objects.all()

        # Pass the data to the template context
        context = {
            'stations': stations,
            'classes': classes,
        }
        return render(request, 'home.html', context)
class UserLogin(View):
    template_name = 'home.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            phone_no = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_no=phone_no, password=password)
            if user is not None:
                login(request, user)
                print("logged in ----")
                return redirect('home')  # Replace 'dashboard' with your desired success URL
            else:
                form.add_error(None, 'Invalid login credentials')

        return render(request, self.template_name, {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('home')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        emails = user.emails.all()
        return render(request, self.template_name, {'user': user, 'emails': emails})

    def post(self, request, *args, **kwargs):
        user = request.user
        emails = request.POST.getlist("emails[]")
        form = UserProfileForm(request.POST, instance=user)
        print(form.errors)
        if form.is_valid():
            form.save()
            email_count = user.emails.count()
            for idx, email in enumerate(emails):
                if idx >= email_count:
                    user.add_user_email(email)

        return redirect('profile')

class SignupView(View):
    template_name = 'home.html'
    form_class = SignupForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # You can perform additional actions after successful registration
            return redirect('home')

        return render(request, self.template_name, {'form': form})

