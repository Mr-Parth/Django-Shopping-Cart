from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from . import serializers
from .models import CustomUser
from .permissions import IsAdminUserProfile

User = CustomUser

# User Registration
@api_view(['POST'])
def register_user(request):
    serializer = serializers.UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        serializer = serializers.UserSerialiser(instance=user)
        return Response({"token": token.key, "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login
@api_view(['POST'])
def login_user(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    serializer = serializers.UserSerialiser(instance=user)
    return Response({"token":token.key, "data": serializer.data})

# Admin: Suspend User
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAdminUserProfile])
def suspend_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if user == request.user:
        return Response({"error": "Can not suspend Self profile"}, status=status.HTTP_400_BAD_REQUEST)

    if user.userprofile.role == "admin":
        return Response({"error": "Can not suspend Admin profile"}, status=status.HTTP_400_BAD_REQUEST)

    user.is_suspended = True
    user.save()
    return Response({"message": "User Suspended"})
