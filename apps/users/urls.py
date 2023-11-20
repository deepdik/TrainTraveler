from django.urls import path

from apps.users.views import HomeView, UserLogin, custom_logout, SignupView, ProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]