from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request,'main/home.html', {})

def login(request):
    return render(request,'main/login.html', {})

def threads_list(request):
    return render(request,'main/threads.html', {})