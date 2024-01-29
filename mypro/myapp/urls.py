from django.urls import path 
from .import views
from .views import User_login,Admin_login

urlpatterns = [
 
    path('userreg',views.userregister),
    path('adminreg',views.Admin_register),
    path('userlogin/', User_login.as_view()),
    path('adminlogin/',Admin_login.as_view()),
    path('send-otp/', views. Send_otp.as_view()),
    path('verify-otp/', views.verify_otp),
    path('create-new-password/<int:id>/', views.create_new_password),
]
