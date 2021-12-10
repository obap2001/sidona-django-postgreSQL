from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', registerAdmin, name='register_admin'),
    path('penggalang_dana/', registerPenggalang,
         name='register_penggalang_dana'),

]
