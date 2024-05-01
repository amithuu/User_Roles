from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserLog, UserRole


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    @receiver(user_logged_in)
    def log_user_login(sender, request, user, **kwargs):
        UserLog.objects.create(user=user, event_type='Login')

    @staticmethod
    @receiver(user_logged_out)
    def log_user_logout(sender, request, user, **kwargs):
        UserLog.objects.create(user=user, event_type='Logout')

    @staticmethod
    @receiver(post_save, sender=User)
    def log_user_role_change(sender, instance, created, **kwargs):
        if not created:
            user_role = UserRole.objects.get(user=instance)
            current_role = user_role.role
            previous_role = UserRole.objects.filter(user=instance).order_by('-created_at').first()
            if current_role != previous_role:
                UserLog.objects.create(user=instance, event_type='Role Change')


# class UserRoleChangeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_response(self, request, response):
#         if request.user.is_authenticated:
#             if hasattr(request.user, 'initial_role'):
#                 if request.user.role != request.user.initial_role:
#                     UserLog.objects.create(user=request.user, event_type='Role Change')
#         return response

# @receiver(user_logged_in)
# def log_user_login(sender, request, user, **kwargs):
#     UserLog.objects.create(user=user, event_type='Login')

# @receiver(user_logged_out)
# def log_user_logout(sender, request, user, **kwargs):
#     UserLog.objects.create(user=user, event_type='Logout')

# @receiver(post_save, sender=User)
# def log_user_role_change(sender, instance, created, **kwargs):
#     if not created:
#         UserLog.objects.create(user=instance, event_type='Role Change')
