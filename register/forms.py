from datetime import date
from django.core.exceptions import ValidationError
import re
from django import forms
from django.db import connection
from django.forms.widgets import Textarea
from django.utils.formats import date_format


def fetch_email_admin():
    existing_email_admin = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT email From sidona.ADMIN;'
        )
        existing_email_admin = cursor.fetchall()  # Will Get all output of the query
    return tuple(existing_email_admin)


def fetch_email_penggalang():
    existing_email_penggalang = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT email From sidona.PENGGALANG_DANA;'
        )
        existing_email_penggalang = cursor.fetchall()  # Will Get all output of the query
    return tuple(existing_email_penggalang)


class adminRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput())
    nama = forms.CharField(max_length=50, required=True,
                           widget=forms.TextInput())
    nomorHP = forms.CharField(
        max_length=50, required=True, widget=forms.NumberInput())

    def clean(self):
        form_data = self.cleaned_data
        for email in fetch_email_admin():
            if email == form_data['email']:
                raise ValidationError(
                    'Maaf, email yang anda gunakan sudah terdaftar! Gunakan email lainnya.')


class penggalangRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=20, required=True, widget=forms.PasswordInput())
    nama = forms.CharField(max_length=50, required=True)
    noHP = forms.CharField(max_length=20, required=True)
    alamat = forms.CharField(widget=forms.Textarea, required=True)
    namaBank = forms.CharField(max_length=20, required=True)
    noRekening = forms.CharField(max_length=20, required=True)
    jenis = forms.ChoiceField(
        choices=(('INDIVIDU', 'INDIVIDU'), ('ORGANISASI', 'ORGANISASI')))

    def clean(self):
        form_data = self.cleaned_data
        for email in fetch_email_penggalang():
            if email == form_data['email']:
                raise ValidationError(
                    'Maaf, email yang anda gunakan sudah terdaftar! Gunakan email lainnya.')


class individuRegisterForm(forms.Form):
    nik = forms.CharField(max_length=20, required=True)
    tglLahir = forms.CharField(widget=forms.DateInput, required=True)
    jenisKelamin = forms.CharField(max_length=1, required=True)
    linkfotoKTP = forms.CharField(widget=forms.URLInput, required=True)


class organisasiRegisterForm(forms.Form):
    namaOrganisasi = forms.CharField(max_length=50, required=True)
    noAkta = forms.CharField(max_length=20, required=True)
    notelp = forms.CharField(max_length=20, required=True)
    tahunBerdiri = forms.CharField(widget=forms.NumberInput, required=True)
    linkFotoAkta = forms.CharField(widget=forms.URLInput, required=True)
