from django.conf.global_settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.db import models
import os
import datetime


def path_wrapper(name):

    def user_directory_path(instance, filename):
        time_now = datetime.datetime.now()
        check_dir = 0

        while default_storage.exists("timestamp_" + time_now.now().strftime("%Y-%b-d_%d-hr_%H") + "id_" + str(check_dir) + "/" + name):
            check_dir += 1

        return "timestamp_" + datetime.datetime.now().strftime("%Y-%b-d_%d-hr_%H") + "id_" + str(check_dir) + "/" + name

    return user_directory_path


class Information(models.Model):
    families = models.FileField(upload_to=(path_wrapper("families")),
                                validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'csv'])])
    chromosomes = models.FileField(upload_to=(path_wrapper("chromosomes")),
                                   validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    colors = models.FileField(upload_to=(path_wrapper("colors")), blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['txt'])])

