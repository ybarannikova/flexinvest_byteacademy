from django.shortcuts import render,redirect

def index(request):
    return render(request, 'main_controller/new.html')

def howitworks(request):
	return render(request, 'main_controller/howitworks.html')