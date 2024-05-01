from django.db import models

import uuid
from timestamps.models import models,Timestampable, SoftDeletes
from proj.helpers.const import * 

# Create your models here.

# class User (Timestampable,SoftDeletes):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField(unique=True)
#     role = models.CharField(max_length=10, unique=True)
#     is_active = models.CharField(max_length=10, default='active', choices = STATUS, null=True)
    
#     class Meta:
#         db_table = 'users'
        
    
# # class Role(Timestampable,SoftDeletes):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     role = models.ForeignKey(User, on_delete=models.CASCADE)
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
# #     class Meta:
# #         db_table = 'UserRole'
        
# class Role(Timestampable,SoftDeletes):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     role = models.ForeignKey(User, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     status = models.CharField(max_length=10)

#     class Meta:
#         db_table = 'user_role'
    
    
# class UserLog(Timestampable,SoftDeletes):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     event = models.CharField(max_length=15)
    
#     class Meta:
#         db_table = 'user_logs'
    
    
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'roles'
        
    def __str__(self):
        return self.name
    


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.CharField(default='disable', choices=STATUS,max_length=10)

    class Meta:
        db_table = 'users_roles'
        unique_together = ('user', 'role')

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'
    


