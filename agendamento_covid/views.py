from django.shortcuts import render
from django.http import HttpResponse

# Create your views herede
def home(request):
    return render(request, 'usuarios/home.html')