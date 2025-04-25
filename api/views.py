from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username')
        return Response({"users":list(users)}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error":"must provide username and password"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error":"User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully", "user_id": user.id},  status=status.HTTP_201_CREATED)

@api_view(['GET'])
@login_required
def secured(request):
    return Response("secured")        