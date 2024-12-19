from django.db import models
from django.contrib.auth.models import  BaseUserManager , AbstractUser
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import get_user_model

class UserProfileManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

# สร้าง Custom User Model
class CustomUser(AbstractUser):
    # เพิ่มฟิลด์เพิ่มเติมที่คุณต้องการ เช่น อีเมล, รูปภาพโปรไฟล์
    email = models.EmailField(max_length=255, blank=True, null=True)

    
    def __str__(self):
        return self.username