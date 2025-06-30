from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} ({self.employee_id})"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)


class QRCodeSession(models.Model):
    token = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=[('checkin', 'Check In'), ('checkout', 'Check Out')])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "QR Code Session"
        verbose_name_plural = "QR Code Sessions"
        
    def is_expired(self):
        return timezone.now() > self.expires_at or not self.is_active
