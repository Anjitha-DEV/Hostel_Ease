from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StudentRegistrationForm, WardenRegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect after successful registration
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_register.html', {'form': form})

def warden_register(request):
    if request.method == 'POST':
        form = WardenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = WardenRegistrationForm()
    return render(request, 'warden_register.html', {'form': form})