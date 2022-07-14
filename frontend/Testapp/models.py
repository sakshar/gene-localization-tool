from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.db import models
import datetime


def read_time(my_time):
    return "timestamp_" + my_time.strftime("%Y-%b-d%d-hr%H-")


def path_wrapper(name):
    def user_directory_path(instance, filename):
        time_now = datetime.datetime.now()
        check_dir = 0

        if not name == "colors":
            while default_storage.exists(read_time(time_now) + "id" + str(check_dir) + "/" + name):
                check_dir += 1
        else:
            while default_storage.exists(read_time(time_now) + "id" + str(check_dir)):
                check_dir += 1
            check_dir -= 1

        return read_time(time_now) + "id" + str(check_dir) + "/" + name

    return user_directory_path


class Information(models.Model):
    families = models.FileField(upload_to=(path_wrapper("families")),
                                validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'csv'])])
    chromosomes = models.FileField(upload_to=(path_wrapper("chromosomes")),
                                   validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    colors = models.FileField(upload_to=(path_wrapper("colors")), blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['txt'])])
