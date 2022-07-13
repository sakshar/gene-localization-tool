import os

from django.core.validators import FileExtensionValidator
from django.db import models
import uuid


def path_wrapper(name, session):

    def user_directory_path(instance, filename):
        return "session_" + session + "/" + name + "/" + filename
    return user_directory_path


class Information(models.Model):
    my_filename = uuid.uuid4().hex

    families = models.FileField(upload_to=(path_wrapper("families", my_filename)),
                                validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'csv'])])
    chromosomes = models.FileField(upload_to=(path_wrapper("chromosomes", my_filename)),
                                   validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    colors = models.FileField(upload_to=(path_wrapper("colors", my_filename)), blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['txt'])])

