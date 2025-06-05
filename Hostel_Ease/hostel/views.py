from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import District, Hostel, Application, Mess
from .forms import StudentRegistrationForm, WardenRegistrationForm, ApplicationForm, HostelRegistrationForm, UserProfileForm, MessForm
from django.contrib import messages

def index(request):
    districts = District.objects.all()
    return render(request, 'index.html', {'districts': districts})

@login_required
def home(request):
    applications = Application.objects.filter(student=request.user) if request.user.role == 'student' else []
    managed_hostels = Hostel.objects.filter(warden=request.user) if request.user.role == 'warden' else []
    pending_applications = Application.objects.filter(
        hostel__warden=request.user, status='pending'
    ) if request.user.role == 'warden' else []
    return render(request, 'home.html', {
        'user': request.user,
        'applications': applications,
        'managed_hostels': managed_hostels,
        'pending_applications': pending_applications
    })

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_register.html', {'form': form})

def warden_register(request):
    if request.method == 'POST':
        form = WardenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration submitted! Await admin approval.")
            return redirect('login')
    else:
        form = WardenRegistrationForm()
    return render(request, 'warden_register.html', {'form': form})

def register(request):
    return render(request, 'register.html')

def hostel_list(request, district_id):
    district = District.objects.get(id=district_id)
    hostels = Hostel.objects.filter(district=district)
    return render(request, 'hostel_list.html', {'district': district, 'hostels': hostels})

@login_required
def apply_hostel(request, hostel_id):
    if request.user.role != 'student':
        messages.error(request, "Only students can apply for hostels.")
        return redirect('hostel_list', district_id=Hostel.objects.get(id=hostel_id).district.id)
    
    hostel = Hostel.objects.get(id=hostel_id)
    if Application.objects.filter(student=request.user, hostel=hostel).exists():
        messages.warning(request, "You have already applied for this hostel.")
        return redirect('hostel_list', district_id=hostel.district.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.hostel = hostel
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('hostel_list', district_id=hostel.district.id)
    else:
        form = ApplicationForm()

    return render(request, 'apply_hostel.html', {'form': form, 'hostel': hostel})

@login_required
def register_hostel(request):
    if request.user.role != 'warden':
        messages.error(request, "Only wardens can register hostels.")
        return redirect('profile')

    if request.method == 'POST':
        hostel_form = HostelRegistrationForm(request.POST, request.FILES)
        mess_form = MessForm(request.POST)

        if hostel_form.is_valid() and mess_form.is_valid():
            hostel = hostel_form.save(commit=False)
            hostel.warden = request.user
            hostel.save()

            mess = mess_form.save(commit=False)
            mess.hostel = hostel
            mess.save()

            messages.success(request, "Hostel and Mess registered successfully!")
            return redirect('profile')
    else:
        hostel_form = HostelRegistrationForm()
        mess_form = MessForm()

    return render(request, 'register_hostel.html', {
        'hostel_form': hostel_form,
        'mess_form': mess_form
    })

@login_required
def profile(request):
    applications = Application.objects.filter(student=request.user) if request.user.role == 'student' else []
    managed_hostels = Hostel.objects.filter(warden=request.user) if request.user.role == 'warden' else []
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {
        'user': request.user,
        'applications': applications,
        'managed_hostels': managed_hostels,
        'form': form
    })

@login_required
def approve_application(request, application_id):
    if request.user.role != 'warden':
        messages.error(request, "Only wardens can approve applications.")
        return redirect('home')
    
    try:
        application = Application.objects.get(id=application_id)
        if application.hostel.warden != request.user:
            messages.error(request, "You can only approve applications for your hostels.")
            return redirect('home')
        
        if application.status != 'pending':
            messages.error(request, "This application is already processed.")
            return redirect('home')
        
        if application.hostel.available_rooms <= 0:
            messages.error(request, f"No rooms available in {application.hostel.name}.")
            return redirect('home')
        
        application.status = 'approved'
        application.hostel.available_rooms -= 1
        application.hostel.save()
        application.save()
        messages.success(request, f"Application from {application.student.username} approved. Room allocated.")
        return redirect('home')
    
    except Application.DoesNotExist:
        messages.error(request, "Application not found.")
        return redirect('home')

@login_required
def reject_application(request, application_id):
    if request.user.role != 'warden':
        messages.error(request, "Only wardens can reject applications.")
        return redirect('home')
    
    try:
        application = Application.objects.get(id=application_id)
        if application.hostel.warden != request.user:
            messages.error(request, "You can only reject applications for your hostels.")
            return redirect('home')
        
        application.status = 'rejected'
        application.save()
        messages.success(request, f"Application from {application.student.username} rejected.")
        return redirect('home')
    
    except Application.DoesNotExist:
        messages.error(request, "Application not found.")
        return redirect('home')
    
@login_required
def view_mess_menu(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
        mess = Mess.objects.get(hostel=hostel)
    except Mess.DoesNotExist:
        messages.error(request, "Mess information not available for this hostel.")
        return redirect('hostel_list', district_id=hostel.district.id)
    
    return render(request, 'mess_menu.html', {'hostel': hostel, 'mess': mess})

# @login_required
# def apply_visitor(request):
#     if request.user.role != 'student':
#         return redirect('home')

#     student = request.user
#     hostel = Hostel.objects.filter(warden=student).first()

#     if not hostel:
#         application = Application.objects.filter(student=student, status='approved').first()
#         if application:
#             hostel = application.hostel


#     if request.method == 'POST':
#         form = VisitorForm(request.POST)
#         if form.is_valid():
#             visitor = form.save(commit=False)
#             visitor.visiting_whom = student
#             visitor.hostel = hostel
#             visitor.save()
#             messages.success(request, "Visitor request submitted.")
#             return redirect('home')
#     else:
#         form = VisitorForm()

#     return render(request, 'apply_visitor.html', {'form': form})

# @login_required
# def view_visitor_requests(request):
#     if request.user.role != 'warden':
#         return redirect('home')

#     hostels = Hostel.objects.filter(warden=request.user)
#     visitor_requests = Visitor.objects.filter(hostel__in=hostels, status='pending')

#     return render(request, 'visitor_requests.html', {'visitor_requests': visitor_requests})

# @login_required
# def approve_visitor(request, visitor_id):
#     visitor = Visitor.objects.get(id=visitor_id)
#     if request.user == visitor.hostel.warden:
#         visitor.status = 'approved'
#         visitor.save()
#     return redirect('visitor_requests')

# @login_required
# def reject_visitor(request, visitor_id):
#     visitor = Visitor.objects.get(id=visitor_id)
#     if request.user == visitor.hostel.warden:
#         visitor.status = 'rejected'
#         visitor.save()
#     return redirect('visitor_requests')