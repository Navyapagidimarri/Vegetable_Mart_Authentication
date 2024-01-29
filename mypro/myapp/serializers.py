from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Orderuserregister,Adminregister,OTPModel

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = Orderuserregister
        fields = ['id','Name', 'email', 'Username', 'Password', 'Confirmpassword']

    def validate(self, data):
        if data['Password'] != data['Confirmpassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        order_user = Orderuserregister.objects.create(
            Name=validated_data['Name'],
            Email=validated_data['email'],
            Username=validated_data['Username'],
            Password=validated_data['Password'],
            Confirmpassword=validated_data['Confirmpassword']
        )
        order_user.save()
        return order_user
    
class User_authserializer(serializers.ModelSerializer):
    class Meta:
        model= Orderuserregister
        fields = ['id','Username','Password']

class Adminserializer(serializers.ModelSerializer):
    class Meta:
        model = Adminregister
        fields = ['id','emp_name', 'emp_email', 'empid', 'Password', 'Confirmpassword']

    def validate(self, data):
        if data['Password'] != data['Confirmpassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        order_user = Admin_register.objects.create(
            emp_name=validated_data['emp_name'],
            emp_email=validated_data['emp_email'],
            empid=validated_data['empid'],
            Password=validated_data['Password'],
            Confirmpassword=validated_data['Confirmpassword']
        )
        order_user.save()
        return order_user

class Admin_authserializer(serializers.ModelSerializer):
    class Meta:
        model= Adminregister
        fields = ['id','empid','Password']


class SendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orderuserregister
        fields=['id','email']
    


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class CreateNewPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orderuserregister
        fields=['id','Password','Confirmpassword']
    
    def validate(self, data):
        if data['Password'] != data['Confirmpassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
