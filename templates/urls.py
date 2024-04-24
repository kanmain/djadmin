from django.urls import path
from . import views 

urlpatterns = [
    path('', views.XView.as_view(), name='xname'),
  ]