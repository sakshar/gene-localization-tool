from django.urls import path
from . import views

urlpatterns = [
    path('', views.v_index, name='index'),
    path('help', views.v_help, name='help'),
    path('about', views.v_about, name='about'),
    path('download', views.v_download, name='download')
]
