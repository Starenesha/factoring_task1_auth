from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.send_phone_number, name="signup_init"),
    path('login/', views.LoginView.as_view(), name='LoginView_url'),
    path('create/', views.RegistrationView.as_view(), name="RegistrationView_url"),
    path('profile/', views.profile_account, name='profile_account_url')
]
