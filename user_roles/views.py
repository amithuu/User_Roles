from django.shortcuts import render

# Create your views here.
from .models import Role, User
from . import serializers 
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

from .mailtrap import simple

class RoleListAPiView(generics.ListAPIView):
    
    serializer_class = serializers.RoleSerializer
    
    def get_queryset(self):
        return Role.objects.all()
    
    def get(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        return Response(data, status=status.HTTP_200_OK)
        
class RolePostAPiView(generics.CreateAPIView):
    
    serializer_class = serializers.RoleSerializer
    
    def post(self, request,*args, **kwargs):
        
        serializer = self.get_serializer(data = request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)






class UserListAPiView(generics.ListAPIView):
    
    serializer_class = serializers.UserSerializer
    
    def get_queryset(self):
        return User.objects.all()
    
    def get(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True).data
        
        return Response(serializer, status=status.HTTP_200_OK)
        
        
class UserPostAPiView(generics.CreateAPIView):
    
    serializer_class = serializers.UserSerializer
    
    def post(self, request,*args, **kwargs):
        
        serializer = self.get_serializer(data = request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
    def get_queryset(self, pk=None):
        obj = self.queryset.filter(pk=pk).all()
        return obj

    def get(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.get_queryset(pk=pk)
            serializer_context = {'request': request}
            serializer = self.get_serializer(instance, context=serializer_context, many=True)
            data = serializer.data
            return Response(data)
        
        except Exception as e:
            return Response({'detail': 'Something went wrong.'}, 500)

    def patch(self, request, pk=None, *args, **kwargs):
        try:
            instance = User.objects.filter(pk=pk).first()
            serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
            
            if not serializer.is_valid(raise_exception=False):
                return ValidationError(serializer.errors)
            
            serializer.save()
            data = serializer.data
            return Response(data)
        
        except Exception as e:
            return Response({'detail': 'Something went wrong.', 'error':str(e)})

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = User.objects.filter(pk=pk).first()
            instance.delete()
            return Response({'detail': 'Object deleted.'})
        
        except Exception as e:
            return Response({'detail': 'Something went wrong.', 'error':str(e)})



class loginAPIView(generics.CreateAPIView):

    def login_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate user
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    
                    send_email = simple(request,data=f'Username: {username}, Password: {password}')
                    # login(request, user)
                    return JsonResponse({'message': 'Login successful', 'success': True, 'email':send_email})
                else:
                    return JsonResponse({'message': 'Your account is disabled', 'success': False})
            else:
                return JsonResponse({'message': 'Invalid username or password', 'success': False})

        return JsonResponse({'message': 'Method not allowed', 'success': False})