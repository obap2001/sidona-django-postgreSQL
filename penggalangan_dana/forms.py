from datetime import date
from uuid import NAMESPACE_DNS
from django.core.exceptions import ValidationError
import re
from django import forms
from django.db import connection
from django.forms import widgets
from django.forms.widgets import Textarea, URLInput
from django.utils.formats import date_format


def fetch_kategori_penggalangan():
    kategori_penggalangan = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''SELECT nama_kategori From sidona.KATEGORI_PD;'''
        )
        kategori_penggalangan = cursor.fetchall()  # Will Get all output of the query

    data_organized = []
    for i in kategori_penggalangan:
        temp = (i[0], f'{i[0]}')
        data_organized.append(temp)
    return tuple(data_organized)


def fetch_kategori_aktifitas():
    kategori_aktifitas = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT nama From sidona.KATEGORI_AKTIVITAS_PD_RUMAH_IBADAH;'
        )
        kategori_aktifitas = cursor.fetchall()  # Will Get all output of the query
    data_organized = []
    for i in kategori_aktifitas:
        temp = (f'{i[0]}', f'{i[0]}')
        data_organized.append(temp)
    return tuple(data_organized)


class KategoriForm(forms.Form):
    kategori = forms.ChoiceField(choices=fetch_kategori_penggalangan())


class OpsiPasienForm(forms.Form):
    pilihan = forms.ChoiceField(choices=(('Ya', 'Ya'), ('Tidak', 'Tidak')))


class PasienForm(forms.Form):
    nIK = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    tanggal_lahir = forms.DateField(required=True)
    alamat = forms.CharField(max_length=50, required=True)
    pekerjaan = forms.CharField(max_length=50, required=True)


class PasienDetailForm(forms.Form):
    nIK = forms.CharField(max_length=20, required=True, disabled=True)
    nama = forms.CharField(max_length=50, required=True, disabled=True)
    tanggal_lahir = forms.DateField(required=True, disabled=True)
    alamat = forms.CharField(max_length=50, required=True, disabled=True)
    pekerjaan = forms.CharField(max_length=50, required=True, disabled=True)


class CekPasienForm(forms.Form):
    nIK_pasien = forms.CharField(max_length=20, required=True)


class OpsiRumahIbadahForm(forms.Form):
    pilihan = forms.ChoiceField(choices=(('Ya', 'Ya'), ('Tidak', 'Tidak')))


class RumahIbadahForm(forms.Form):
    nomor_sertifikat = forms.CharField(max_length=20, required=True)
    nama = forms.CharField(max_length=50, required=True)
    alamat = forms.CharField(max_length=50, required=True)
    jenis = forms.CharField(max_length=50, required=True)


class CekRumahIbadahForm(forms.Form):
    nomor_sertifikat_rumah_ibadah = forms.CharField(
        max_length=20, required=True)


class RumahIbadahDetailForm(forms.Form):
    nomor_sertifikat = forms.CharField(
        max_length=20, required=True, disabled=True)
    nama = forms.CharField(max_length=50, required=True, disabled=True)
    alamat = forms.CharField(max_length=50, required=True, disabled=True)
    jenis = forms.CharField(max_length=50, required=True, disabled=True)


class PenggalanganDanaForm(forms.Form):
    iD_penggalangan_dana = forms.CharField(
        max_length=20, required=True, disabled=True)
    email_penggalangan_dana = forms.EmailField(
        disabled=True)
    judul = forms.CharField(widget=forms.Textarea, required=True)
    deskripsi = forms.CharField(widget=forms.Textarea, required=True)
    kota = forms.CharField(max_length=50, required=True)
    provinsi = forms.CharField(max_length=50, required=True)
    deadline_penggalangan_dana = forms.CharField(
        widget=forms.DateInput, required=True)
    jumlah_target_dana = forms.CharField(label="Jumlah Target Dana (Rp)",
                                         widget=forms.NumberInput, required=True)


class DataTambahanPDKesehatanForm(forms.Form):
    kategori = forms.CharField(max_length=20, required=True, disabled=True)
    nIK_pasien = forms.CharField(max_length=20, required=True, disabled=True)
    nama_pasien = forms.CharField(max_length=50, required=True, disabled=True)
    penyakit_utama = forms.CharField(
        max_length=50, required=True)
    link_berkas_penggalangan_dana = forms.URLField(required=True)


class DataTambahanPDRIForm(forms.Form):
    kategori = forms.CharField(max_length=20, required=True, disabled=True)
    nomor_sertifikat_rumah_ibadah = forms.CharField(
        max_length=20, required=True, disabled=True)
    kategori_aktivitas = forms.ChoiceField(
        choices=fetch_kategori_aktifitas(), required=True)
    link_berkas_penggalangan_dana = forms.URLField(required=True)


class DataTambahanPDForm(forms.Form):
    kategori = forms.CharField(max_length=20, required=True, disabled=True)
    link_berkas_penggalangan_dana = forms.CharField(
        widget=URLInput, required=True)


class DetailPenggalanganDanaForm(forms.Form):
    iD_penggalangan_dana = forms.CharField(
        max_length=20, required=True, disabled=True)
    email_penggalangan_dana = forms.EmailField(
        disabled=True)
    judul = forms.CharField(widget=forms.Textarea,
                            required=True, disabled=True)
    deskripsi = forms.CharField(
        widget=forms.Textarea, required=True, disabled=True)
    kota = forms.CharField(max_length=50, required=True, disabled=True)
    provinsi = forms.CharField(max_length=50, required=True, disabled=True)
    deadline_penggalangan_dana = forms.CharField(
        widget=forms.DateInput, required=True, disabled=True)
    jumlah_target_dana = forms.CharField(label="Jumlah Target Dana (Rp)",
                                         widget=forms.NumberInput, required=True, disabled=True)


class DetailTambahanPDKesehatanForm(forms.Form):
    kategori = forms.CharField(max_length=20, required=True, disabled=True)
    nIK_pasien = forms.CharField(max_length=20, required=True, disabled=True)
    nama_pasien = forms.CharField(max_length=50, required=True, disabled=True)
    penyakit_utama = forms.CharField(
        max_length=50, required=True, disabled=True)
    komorbid = forms.CharField(max_length=50, required=True, disabled=True)
    link_berkas_penggalangan_dana = forms.CharField(
        widget=URLInput, required=True, disabled=True)
    jumlah_terkumpul = forms.CharField(
        max_length=20, required=True, disabled=True)
    jumlah_terpakai = forms.CharField(
        max_length=20, required=True, disabled=True)


class DetailTambahanPDRIForm(forms.Form):
    kategori = forms.CharField(max_length=20, required=True, disabled=True)
    nomor_sertifikat_rumah_ibadah = forms.CharField(
        max_length=20, required=True, disabled=True)
    kategori_aktivitas = forms.ChoiceField(
        choices=fetch_kategori_aktifitas(), required=True, disabled=True)
    link_berkas_penggalangan_dana = forms.CharField(
        widget=URLInput, required=True, disabled=True)
    jumlah_terkumpul = forms.CharField(
        max_length=20, required=True, disabled=True)
    jumlah_terpakai = forms.CharField(
        max_length=20, required=True, disabled=True)


class DetailTambahanPDForm(forms.Form):
    kategori = forms.CharField(max_length=20, required=True, disabled=True)
    link_berkas_penggalangan_dana = forms.CharField(
        widget=URLInput, required=True, disabled=True)
    jumlah_terkumpul = forms.CharField(
        max_length=20, required=True, disabled=True)
    jumlah_terpakai = forms.CharField(
        max_length=20, required=True, disabled=True)
