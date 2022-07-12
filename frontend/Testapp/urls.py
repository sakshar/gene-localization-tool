from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.v_index, name='index'),
    path('help', views.v_help, name='help'),
    path('about', views.v_about, name='about'),
    # path('confirm', views.v_confirm, name='confirm')
    path('download', views.v_download, name='download')
]