


from django.db import models

# Create your models here.
class Orderuserregister(models.Model):
    Name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    Username=models.CharField(max_length=50)
    Password=models.CharField(max_length=50)
    Confirmpassword=models.CharField(max_length=50)  

class Adminregister(models.Model):
    emp_name=models.CharField(max_length=100)
    emp_email=models.EmailField(max_length=100)
    emp_id=models.CharField(max_length=50)
    Password=models.CharField(max_length=50)
    Confirmpassword=models.CharField(max_length=50)

class OTPModel(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email}"