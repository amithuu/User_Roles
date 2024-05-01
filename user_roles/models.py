from django.contrib.auth import models
from timestamps.models import models,Timestampable, SoftDeletes
import uuid
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
class User(AbstractUser,Timestampable,SoftDeletes):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
    
    
    def __str__(self):
        return self.email


class Role(Timestampable, SoftDeletes):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return self.name


class UserRole(Timestampable, SoftDeletes):
    # id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_roles'
    
    def __str__(self):
        return self.user.username + '' + self.role.name
    
    
class UserLog(Timestampable, SoftDeletes):
    # id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_log'
    
    def __str__(self):
        return self.user.username + "" + self.event_type
    
    
    