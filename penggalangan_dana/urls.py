from django.urls import path
from .views import *

urlpatterns = [
    path('', kategori_view, name='kategori'),
    path('opsi_kesehatan/<str:kategori>', opsi_pasien, name='opsi_pasien'),
    path('opsi_rumah_ibadah/<str:kategori>',
         opsi_rumah_ibadah, name='opsi_rumah_ibadah'),
    path('add_pasien/<str:kategori>', add_pasien, name='add_pasien'),
    path('add_rumah_ibadah/<str:kategori>',
         add_rumah_ibadah, name='add_rumah_ibadah'),
    path('check_pasien/<str:kategori>', check_pasien, name='check_pasien'),
    path('check_rumah_ibadah/<str:kategori>',
         check_rumah_ibadah, name='check_rumah_ibadah'),
    path('detail_pasien/<str:nik>/<str:kategori>/<str:nama>',
         pasien_detail, name='detail_pasien'),
    path('detail_rumah_ibadah/<str:nosertif>/<str:kategori>',
         rumah_ibadah_detail, name='detail_rumah_ibadah'),
    path('create/<str:kategori>/<str:id>/<str:nama>',
         create_penggalangan, name='create_penggalangan'),
    path('create/<str:kategori>/<str:id>',
         create_penggalangan, name='create_penggalangan'),
    path('create/<str:kategori>',
         create_penggalangan, name='create_penggalangan'),
    path('list_penggalangan/', list_penggalangan, name='list_penggalangan'),
    path('detail_penggalangan/<str:id>/',
         detail_penggalangan, name='detail_penggalangan'),
    path('delete_penggalangan/<str:kategori>/<str:id>/',
         delete_penggalangan, name='delete_penggalangan'),
    path('delete_penggalangan/<str:kategori>/',
         delete_penggalangan, name='delete_penggalangan'),


]
