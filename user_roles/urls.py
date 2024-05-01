from django.urls import path
from . import views

urlpatterns = [
    path('roleslist/', views.RoleListAPiView.as_view(), name='user-list'),
    path('rolescreate/', views.RolePostAPiView.as_view(), name='role-create'),
    path('userslist/', views.UserListAPiView.as_view(), name='user-list'),
    path('userscreate/', views.UserPostAPiView.as_view(), name='user-create'),
    path('users/<pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('login/', views.loginAPIView.as_view(), name='Login'),
    
]
