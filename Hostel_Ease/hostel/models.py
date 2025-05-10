from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('warden', 'Warden'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.username} ({self.role})"
    

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def _str_(self):
        return self.name 
    
class Hostel(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    available_rooms = models.PositiveIntegerField()
    total_rooms = models.PositiveIntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    warden = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_hostels')

    def __str__(self):
        return self.name
    
class Mess(models.Model):
    hostel = models.OneToOneField(Hostel, on_delete=models.CASCADE)
    menu = models.TextField()
    monthly_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def _str_(self):
        return f"Mess for {self.hostel.name}"
    
class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    visit_date = models.DateTimeField(auto_now_add=True)
    visiting_whom = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    reason = models.TextField()

    def _str_(self):
        return f"{self.name} visiting {self.visiting_whom.username}"
    
class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def _str_(self):
        return f"{self.student.username} -> {self.hostel.name} ({self.status})"