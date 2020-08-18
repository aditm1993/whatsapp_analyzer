from django.contrib import admin
from django.urls import path
from whatsapp_analyzer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('send-file', views.send_file, name='send-file'),
]
