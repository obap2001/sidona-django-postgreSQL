from django.urls import path
from .views import *

urlpatterns = [
    path('', komorbid_view, name='komorbid'),
    path('create/<str:email>', add_komorbid, name='add_komorbid'),

]
