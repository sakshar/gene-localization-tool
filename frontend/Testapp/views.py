from django.shortcuts import render, redirect
from .forms import InformationForm
import os
import datetime
from django.core.files.storage import default_storage


def v_index(request):
    if request.method == 'POST':
        new_information = InformationForm(request.POST, request.FILES)
        if new_information.is_valid():
            new_information.clean()
            new_information.save()

            directory = get_directory()
            colors_path = "media\\" + directory + "\\colors"
            families_path = "media\\" + directory + "\\families"
            chromosomes_path = "media\\" + directory + "\\chromosomes"
            if default_storage.exists(directory + "/colors"):
                os.system('python ..\\backend\\geneLocalization.py' + ' ' + families_path + ' ' + chromosomes_path + ' ' + colors_path)
            else:
                os.system('python ..\\backend\\geneLocalization.py' + ' ' + families_path + ' ' + chromosomes_path)

            return redirect('./download')
    else:
        new_information = InformationForm()
    return render(request, 'index.html', {'form': new_information})


def v_download(request):
    # check for most recent upload and store name of directory

    context = {
        "pdf_path": "",
        "png_path": ""
    }
    return render(request, 'download.html', context)


def v_about(request):
    return render(request, 'about.html')


def v_help(request):
    return render(request, 'help.html')


def get_directory():
    check_dir = 0
    timestamp = "timestamp_" + datetime.datetime.now().strftime("%Y-%b-d%d-hr%H-")
    while default_storage.exists(timestamp + "id" + str(check_dir)):
        check_dir += 1
    return timestamp + "id" + str(check_dir - 1)
