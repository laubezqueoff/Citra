from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request,'home.html', {})

def login(request):
    return render(request,'login.html', {})

def chat(request):
    return render(request,'chat.html',{})
  
def threads_list(request):
    return render(request,'threads.html', {})
