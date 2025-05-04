from django.urls import path
from .views import home,warden_register,student_register

urlpatterns = [
    path('', home, name='home'),
    path('register/student/', student_register, name='student'),
    path('register/warden/', warden_register, name='warden'),
]