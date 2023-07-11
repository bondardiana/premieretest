from django.urls import path

from . import views
from mycalc.views import calculation

urlpatterns = [
  # path('', views.index, name='index'),
   path('calculation/',  calculation, name='calculation'),

]