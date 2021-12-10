from collections import namedtuple
import datetime
from re import template
from django.http import request, response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, InternalError
from datetime import datetime

from komorbid.forms import CreateKomorbidForm

# Create your views here.


def komorbid_view(request):
    response = {}
    data_komorbid = []
    data_komorbid_all = []

    email = request.session['email']
    if request.session['peran'] == 'PENGGALANG DANA':
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT * FROM PENGGALANGAN_DANA_PD JOIN KOMORBID ON id = idpd
                NATURAL JOIN PASIEN NATURAL JOIN PD_KESEHATAN
                WHERE email_user = '{email}';
                ''')
            data_komorbid = cursor.fetchall()
        data_organized = []
        num = 1
        for i in data_komorbid:
            if num < 10:
                temp = ('K-00'+str(num), i[2], i[18], i[24])
                num = + 1
            elif num < 100:
                temp = ('K-0'+str(num), i[2], i[18], i[24])
                num = +1
            else:
                temp = ('K-'+str(num), i[2], i[18], i[24])
                num = + 1
            data_organized.append(temp)
        response['title'] = 'Kelola Penyakit Komorbid'
        response['data_komorbid'] = data_organized

    elif request.session['peran'] == 'ADMIN':
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT DISTINCT judul, penyakit, komorbid FROM PENGGALANGAN_DANA_PD JOIN KOMORBID ON id = idpd
                NATURAL JOIN PASIEN NATURAL JOIN PD_KESEHATAN;
                ''')
            data_komorbid_all = cursor.fetchall()

        data_organized_all = []
        num1 = 1
        for i in data_komorbid_all:
            if num1 < 10:
                temp = ('K-00'+str(num1), i[0], i[1], i[2])
                num1 = + 1
            elif num1 < 100:
                temp = ('K-0'+str(num1), i[0], i[1], i[2])
                num1 = +1
            else:
                temp = ('K-'+str(num1), i[0], i[1], i[2])
                num1 = + 1
            data_organized_all.append(temp)
        response['title1'] = 'Daftar Penyakit Komorbid'
        response['data_komorbid_all'] = data_organized_all
    response['email'] = email
    return render(request, 'list_komorbid.html', response)


def add_komorbid(request, email):
    response = {}
    form = CreateKomorbidForm(request.POST or None)

    response['title'] = 'Informasi Penyakit Komorbid'
    response['form'] = form

    if request.method == 'POST' and form.is_valid():
        idpd = form.cleaned_data['idpd']
        komorbid = form.cleaned_data['komorbid']

        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                INSERT INTO KOMORBID values
                ('{idpd}','{komorbid}')
                ;'''
            )
        return redirect('komorbid')
    return render(request, 'add_komorbid.html', response)
