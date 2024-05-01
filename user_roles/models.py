from django.contrib.auth import models
from timestamps.models import models,Timestampable, SoftDeletes
import uuid

class User(Timestampable,SoftDeletes):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.username


class Role(Timestampable, SoftDeletes):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return self.name


class UserRole(Timestampable, SoftDeletes):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_roles'
    
    def __str__(self):
        return f"{self.user} - {self.role}"
    
    
class UserLog(Timestampable, SoftDeletes):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_log'
    
    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.timestamp}"