from django.urls import path
from .views import (
    home, warden_register, student_register, hostel_list, apply_hostel, 
    index, register, profile, register_hostel, approve_application, reject_application, view_mess_menu
)

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('register/student/', student_register, name='student_register'),
    path('register/warden/', warden_register, name='warden_register'),
    path('register/', register, name='register'),
    path('hostels/<int:district_id>/', hostel_list, name='hostel_list'),
    path('hostels/apply/<int:hostel_id>/', apply_hostel, name='apply_hostel'),
    path('hostels/register/', register_hostel, name='register_hostel'),
    path('profile/', profile, name='profile'),
    path('applications/approve/<int:application_id>/', approve_application, name='approve_application'),
    path('applications/reject/<int:application_id>/', reject_application, name='reject_application'),
    path('hostel/<int:hostel_id>/mess/', view_mess_menu, name='view_mess_menu'),
]