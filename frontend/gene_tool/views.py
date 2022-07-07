from django.shortcuts import render
from django.http import HttpResponse


def v_help(request):
    return render(request, 'help.html')


def v_index(request):
    return render(request, 'index.html')

def v_about(request):
    return render(request, 'about.html')