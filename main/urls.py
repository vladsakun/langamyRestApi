import django
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    path('login/', TemplateView.as_view(template_name="login/login.html"), name='login_url'),
    path('', views.index),
    path('get/dictation/<int:code>/', views.get_dictation, name="get_dictation_url"),
    path('dictation/<int:code>/', views.dictation, name="get_dictation_url")
]
