from django.db import models
import uuid

data_id = uuid.uuid4().hex


class Information(models.Model):
    families = models.FileField(upload_to=('session_' + data_id + '/' + 'families'))
    chromosomes = models.FileField(upload_to=('session_' + data_id + '/' + 'chromosomes'))
    colors = models.FileField(upload_to=('session_' + data_id + '/' + 'colors'), blank=True, null=True)

