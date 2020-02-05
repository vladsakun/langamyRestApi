from django.conf.urls import url
from django.urls import path

from api import views

urlpatterns = [
    path('api/get/specific_studyset/<int:pk>/', views.api_study_set_detail),
    path('api/create/studyset/', views.create_study_set),
    path('api/get/studysetsnames/<str:user_email>/', views.GetStudySetsOfCurrentUser.as_view()),
]
