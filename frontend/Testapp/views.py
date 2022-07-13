from django.shortcuts import render, redirect
from .forms import InformationForm
from django.http import HttpResponse


def v_help(request):
    return render(request, 'help.html')


def v_index(request):
    if request.method == 'POST':
        new_information = InformationForm(request.POST, request.FILES)
        if new_information.is_valid():
            new_information.clean()
            new_information.save()
            #   exec(backend files)
            return redirect('./download')
    else:
        new_information = InformationForm()
    return render(request, 'index.html', {'form': new_information})


def v_download(request):
    return HttpResponse("downloads!")


def v_about(request):
    return render(request, 'about.html')


