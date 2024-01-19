from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from .models import Orderuserregister,Adminregister,OTPModel
from .serializers import Userserializer,Adminserializer,User_authserializer,Admin_authserializer,SendOTPSerializer,VerifyOTPSerializer,CreateNewPasswordSerializer

@api_view(['GET', 'POST'])
def userregister(request):
    if request.method == 'GET':
        mnc = Orderuserregister.objects.all()
        serializer = Userserializer(mnc, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer_user = Userserializer(data=request.data)
        if serializer_user.is_valid():
            serializer_user.save()
            
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
    
class User_login(APIView):
    queryset = Orderuserregister.objects.all()
    serializer_class = User_authserializer
    permission_classes = [AllowAny]

    def post(self, request, args, *kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):

            input_data = serializer.validated_data
            username = input_data.get('Username')
            password = input_data.get('Password')
            user = Orderuserregister.objects.get(Username=username,Password=password)
            return Response({
                "id":user.id,
                "Name":user.Name,
                "Email":user.Email,

            })

@api_view(['GET', 'POST'])
def adminregister(request):
    if request.method == 'GET':
        mnc = adminregister.objects.all()
        serializer = Adminserializer(mnc, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer_user = Adminserializer(data=request.data)
        if serializer_user.is_valid():
            serializer_user.save()
            
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Admin_login(APIView):
    queryset = Adminregister.objects.all()
    serializer_class = Admin_authserializer
    permission_classes = [AllowAny]

    def post(self, request, args, *kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):

            input_data = serializer.validated_data
            empid = input_data.get('emp_id')
            password = input_data.get('Password')
            user = Adminregister.objects.get(emp_id=empid,Password=password)
            return Response({
                "id":user.id,
                "Name":user.emp_name,
                "Email":user.emp_email,

            })
        
@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    print(request.data)
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = str(random.randint(1000, 9999))
        otp_model, created = OTPModel.objects.get_or_create(email=email)
        otp_model.otp = otp
        otp_model.save()
        subject = 'Your OTP for Password Reset'
        message = f'Your OTP is: {otp}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return Response({'detail': 'OTP sent successfully.'})
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user_otp = serializer.validated_data['otp']
        try:
            otp_model = OTPModel.objects.get(email=email)
        except OTPModel.DoesNotExist:
            return Response({'detail': 'Invalid email or OTP.'}, status=400)

        stored_otp = otp_model.otp
        if user_otp == stored_otp:
            return Response({'detail': 'OTP verification successful.'})
        else:
            return Response({'detail': 'Invalid OTP.'}, status=400)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_password(request):
    serializer = CreateNewPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        token = serializer.validated_data.get('token') 
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=400)
        user.set_password(password)
        user.save()  
        OTPModel.objects.filter(email=email).delete()

        return Response({'detail': 'Password reset successfully.'})
    else:
        return Response(serializer.errors, status=400)