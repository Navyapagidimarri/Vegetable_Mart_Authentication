from django.urls import path 
from .import views
from .views import User_login,Admin_login

urlpatterns = [
 
    path('userreg',views.userregister),
    path('adminreg',views.adminregister),
    path('userlogin', User_login.as_view()),
    path('adminlogin',Admin_login.as_view()),
    path('send-otp/', views.send_otp),
    path('verify-otp/', views.verify_otp),
    path('create-new-password/', views.create_new_password),
]