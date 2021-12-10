from collections import namedtuple
import datetime
from re import template
from django.http import request, response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, InternalError
from datetime import datetime

# Create your views here.
from .forms import *


def kategori_view(request):
    response = {}
    form = KategoriForm(request.POST or None)

    # Assigning data for response
    response['form'] = form
    response['title'] = 'Kategori Penggalangan Dana'

    # kategori_pd = ""
    if request.method == 'POST' and form.is_valid():
        kategori_pd = form.cleaned_data['kategori']
        request.session['kategori'] = kategori_pd
        if kategori_pd == "kesehatan":
            return redirect('opsi_pasien', kategori_pd)

        elif kategori_pd == "rumah ibadah":
            return redirect('opsi_rumah_ibadah', kategori_pd)
        else:
            return redirect('create/' + kategori_pd)

    return render(request, 'pilih_kategori.html', response)


def opsi_pasien(request, kategori):
    response = {}
    form_opsi = OpsiPasienForm(request.POST or None)

    response['form'] = form_opsi
    response['title'] = 'Apakah anda ingin memasukkan data pasien baru?'

    if request.method == "POST" and form_opsi.is_valid():
        pilihan = form_opsi.cleaned_data['pilihan']
        if pilihan == "Ya":
            return redirect('add_pasien', kategori)
        else:
            return redirect('check_pasien', kategori)

    return render(request, 'opsi_pasien.html', response)


def add_pasien(request, kategori):
    response = {}
    form_pasien = PasienForm(request.POST or None)

    response['form'] = form_pasien
    response['title'] = 'Identitas Pasien'

    if request.method == 'POST' and form_pasien.is_valid():
        nik = form_pasien.cleaned_data['nIK']
        nama = form_pasien.cleaned_data['nama']
        tgl_lahir = form_pasien.cleaned_data['tanggal_lahir']
        alamat = form_pasien.cleaned_data['alamat']
        pekerjaan = form_pasien.cleaned_data['pekerjaan']
        emailpenggalang = request.session['email']
        # Execute Querry
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''
                    insert into pasien values
                    ('{nik}', '{nama}', '{tgl_lahir}', '{alamat}', '{pekerjaan}');
                    '''
                )
            except InternalError:
                cursor.execute(
                    f'''set search_path to sidona;
                    SELECT nama FROM pasien JOIN pd_kesehatan on nik = idpd
                    JOIN penggalangan_dana_pd on id = idpd
                    WHERE nik='{nik}' and email_user = '{emailpenggalang}';'''
                )
                data = cursor.fetchone()
                if data:
                    messages.error(
                        request, 'Maaf, pasien sudah terdaftar.')

        return redirect('create_penggalangan', kategori, nik, nama)

    return render(request, 'add_pasien.html', response)


def check_pasien(request, kategori):
    response = {}
    form = CekPasienForm(request.POST or None)

    response['form'] = form
    response['title'] = 'Cek Pasien Terdaftar'

    if request.method == 'POST' and form.is_valid():
        nik = form.cleaned_data['nIK_pasien']
        emailpenggalang = request.session['email']

        with connection.cursor() as cursor:
            cursor.execute(
                f'''set search_path to sidona;
                SELECT nama FROM pasien JOIN pd_kesehatan on nik = idpasien
                JOIN penggalangan_dana_pd on id = idpd
                WHERE nik='{nik}' and email_user = '{emailpenggalang}';'''
            )
            data = cursor.fetchone()
            if data:
                return redirect('detail_pasien', nik, kategori, data[0])
            else:
                messages.error(
                    request, 'Maaf, pasien tidak ditemukan. Silahkan coba lagi!')

    return render(request, 'check_pasien.html', response)


def fetch_data_pasien(request, nik):
    data_pasien = []
    emailpenggalang = request.session['email']

    with connection.cursor() as cursor:
        cursor.execute(f'''
             SELECT * from pasien JOIN pd_kesehatan on nik = idpasien
             JOIN penggalangan_dana_pd on id = idpd
             WHERE nik = '{nik}' and email_user = '{emailpenggalang}';
        ''')
        data_pasien = cursor.fetchone()
    if not data_pasien:
        return False

    init_pasien_data = {
        'nIK': data_pasien[0],
        'nama': data_pasien[1],
        'tanggal_lahir': data_pasien[2],
        'alamat': data_pasien[3],
        'pekerjaan': data_pasien[4],

    }
    return init_pasien_data


def pasien_detail(request, nik, kategori, nama):
    response = {}
    data_pasien = fetch_data_pasien(request, nik)
    form = PasienDetailForm(request.POST or None, initial=data_pasien)

    response['form'] = form
    response['title'] = 'Detail Pasien'

    if request.method == 'POST' and form.is_valid():
        return redirect('create_penggalangan', kategori, nik, nama)

    return render(request, 'detail_pasien.html', response)


def opsi_rumah_ibadah(request, kategori):
    response = {}
    form = OpsiRumahIbadahForm(request.POST or None)

    response['form'] = form
    response['title'] = 'Apakah anda ingin memasukkan data rumah ibadah baru?'

    if request.method == 'POST' and form.is_valid():
        pilihan = form.cleaned_data['pilihan']
        if pilihan == 'Ya':
            return redirect('add_rumah_ibadah', kategori)
        else:
            return redirect('check_rumah_ibadah', kategori)

    return render(request, 'opsi_rumah_ibadah.html', response)


def add_rumah_ibadah(request, kategori):
    response = {}
    form = RumahIbadahForm(request.POST or None)

    response['form'] = form
    response['title'] = 'Informasi Rumah Ibadah'

    if request.method == 'POST' and form.is_valid():
        nosertif = form.cleaned_data['nomor_sertifikat']
        nama = form.cleaned_data['nama']
        alamat = form.cleaned_data['alamat']
        jenis = form.cleaned_data['jenis']
        emailpenggalang = request.session['email']

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''
                insert into sidona.rumah_ibadah values
                ('{nosertif}', '{nama}', '{alamat}', '{jenis}');
                '''
                )
            except InternalError:
                cursor.execute(
                    f'''set search_path to sidona;
                SELECT nama FROM rumah_ibadah JOIN pd_rumah_ibadah 
                ON idrumahibadah = nosertifikat JOIN penggalangan_dana_pd
                ON idpd = id
                WHERE nosertifikat='{nosertif}' and email_user = '{emailpenggalang}';'''
                )
                data = cursor.fetchone()
                if data:
                    messages.error(
                        request, 'Maaf, rumah ibadah sudah terdaftar.')

        return redirect('create_penggalangan', kategori, nosertif)

    return render(request, 'add_rumah_ibadah.html', response)


def check_rumah_ibadah(request, kategori):
    response = {}
    form = CekRumahIbadahForm(request.POST or None)

    response['form'] = form
    response['title'] = 'Cek Rumah Ibadah Terdaftar'

    if request.method == 'POST' and form.is_valid():
        nosertif = form.cleaned_data['nomor_sertifikat_rumah_ibadah']
        emailpenggalang = request.session['email']

        with connection.cursor() as cursor:
            cursor.execute(
                f'''set search_path to sidona;
                SELECT nama FROM rumah_ibadah JOIN pd_rumah_ibadah 
                ON idrumahibadah = nosertifikat JOIN penggalangan_dana_pd
                ON idpd = id
                WHERE nosertifikat='{nosertif}' and email_user = '{emailpenggalang}';'''
            )
            data = cursor.fetchone()
            if data:
                return redirect('detail_rumah_ibadah', nosertif, kategori)
            else:
                messages.error(
                    request, 'Maaf, rumah ibadah tidak ditemukan. Silahkan coba lagi!')

    return render(request, 'check_rumah_ibadah.html', response)


def fetch_data_rumah_ibadah2(request, nosertif):
    data_rumah_ibadah = []
    emailpenggalang = request.session['email']

    with connection.cursor() as cursor:
        cursor.execute(f'''
            set search_path to sidona;
             SELECT * from rumah_ibadah JOIN pd_rumah_ibadah 
                ON idrumahibadah = nosertifikat JOIN penggalangan_dana_pd
                ON idpd = id
             WHERE nosertifikat = '{nosertif}' and email_user = '{emailpenggalang}';
        ''')
        data_rumah_ibadah = cursor.fetchone()
    if not data_rumah_ibadah:
        return False

    init_rumah_ibadah_data = {
        'nomor_sertifikat': data_rumah_ibadah[0],
        'nama': data_rumah_ibadah[1],
        'alamat': data_rumah_ibadah[2],
        'jenis': data_rumah_ibadah[3],

    }
    return init_rumah_ibadah_data


def rumah_ibadah_detail(request, nosertif, kategori):
    response = {}
    data_rumah_ibadah = fetch_data_rumah_ibadah2(request, nosertif)
    form = RumahIbadahDetailForm(
        request.POST or None, initial=data_rumah_ibadah)

    response['form'] = form
    response['title'] = 'Detail Rumah Ibadah'

    if request.method == 'POST' and form.is_valid():
        return redirect('create_penggalangan', kategori, nosertif)

    return render(request, 'detail_rumah_ibadah.html', response)


def fetch_kategori_penggalangan():
    kategori_penggalangan = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id, nama_kategori From sidona.KATEGORI_PD;'
        )
        kategori_penggalangan = cursor.fetchall()  # Will Get all output of the query
    return tuple(kategori_penggalangan)


def fetch_kategori_aktifitas():
    kategori_aktifitas = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id, nama From sidona.KATEGORI_AKTIVITAS_PD_RUMAH_IBADAH;'
        )
        kategori_aktifitas = cursor.fetchall()  # Will Get all output of the query
    return tuple(kategori_aktifitas)


def create_penggalangan(request, kategori, id="noId", nama="noName"):
    response = {}

    existing_id = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id From sidona.PENGGALANGAN_DANA_PD;'
        )
        existing_id = cursor.fetchall()
    stringID = ""
    last_id = 0
    for rawId in existing_id:
        idraw = rawId[0]
        fullId = idraw[2:]
        if last_id < int(fullId) and last_id < 9:
            last_id = int(fullId) + 1
            stringID = "00"+str(last_id)
        elif last_id < int(fullId) and last_id < 99:
            last_id = int(fullId) + 1
            stringID = "0"+str(last_id)
        else:
            last_id = int(fullId) + 1
            stringID = str(last_id)
    emailpenggalang = request.session['email']

    if kategori == 'kesehatan':
        init_data_utama = {
            'iD_penggalangan_dana': "K-" + stringID,
            'email_penggalangan_dana': emailpenggalang,
        }
    elif kategori == 'rumah ibadah':
        init_data_utama = {
            'iD_penggalangan_dana': "RI-" + stringID,
            'email_penggalangan_dana': emailpenggalang,
        }
    elif kategori == 'bencana':
        init_data_utama = {
            'iD_penggalangan_dana': "B-" + stringID,
            'email_penggalangan_dana': emailpenggalang,
        }
    elif kategori == 'pendidikan':
        init_data_utama = {
            'iD_penggalangan_dana': "P-" + stringID,
            'email_penggalangan_dana': emailpenggalang,
        }
    else:
        init_data_utama = {
            'iD_penggalangan_dana': "S-" + stringID,
            'email_penggalangan_dana': emailpenggalang,
        }

    if kategori == 'kesehatan':
        init_data_tambahan = {
            'kategori': kategori,
            'nIK_pasien': id,
            'nama_pasien': nama,
        }
    elif kategori == 'rumah ibadah':
        init_data_tambahan = {
            'kategori': kategori,
            'nomor_sertifikat_rumah_ibadah': id,
        }
    else:
        init_data_tambahan = {
            'kategori': kategori,
        }

    form = PenggalanganDanaForm(request.POST or None, initial=init_data_utama)
    if kategori == 'kesehatan':
        form1 = DataTambahanPDKesehatanForm(
            request.POST or None, initial=init_data_tambahan)
    elif kategori == 'rumah ibadah':
        form1 = DataTambahanPDRIForm(
            request.POST or None, initial=init_data_tambahan)
    else:
        form1 = DataTambahanPDForm(
            request.POST or None, initial=init_data_tambahan)

    response['form'] = form
    response['form1'] = form1
    response['title'] = 'Pendaftaran Penggalangan Dana'

    if request.method == 'POST' and form.is_valid() and form1.is_valid():
        id = form.cleaned_data['iD_penggalangan_dana']
        judul = form.cleaned_data['judul']
        deskripsi = form.cleaned_data['deskripsi']
        kota = form.cleaned_data['kota']
        provinsi = form.cleaned_data['provinsi']
        deadline = form.cleaned_data['deadline_penggalangan_dana']
        targetnominal = form.cleaned_data['jumlah_target_dana']
        kategori = form1.cleaned_data['kategori']
        allkategori = fetch_kategori_penggalangan()
        all
        if kategori == 'kesehatan' and allkategori[0][1] == kategori:
            nik = form1.cleaned_data['nIK_pasien']
            nama = form1.cleaned_data['nama_pasien']
            penyakit = form1.cleaned_data['penyakit_utama']
            id_kategori = allkategori[0][0]
        elif kategori == 'rumah ibadah' and allkategori[1][1] == kategori:
            nosertif = form1.cleaned_data['nomor_sertifikat_rumah_ibadah']
            kategori_aktivitas = form1.cleaned_data['kategori_aktivitas']
            id_kategori = allkategori[1][0]
            allaktifitas = fetch_kategori_aktifitas()
            for akt in allaktifitas:
                if akt[1] == kategori_aktivitas:
                    idaktifitas = akt[0]
        elif kategori == 'bencana' and allkategori[2][1] == kategori:
            id_kategori = allkategori[2][0]
        elif kategori == 'pendidikan' and allkategori[3][1] == kategori:
            id_kategori = allkategori[3][0]
        else:
            id_kategori = allkategori[4][0]

        berkas = form1.cleaned_data['link_berkas_penggalangan_dana']
        email_user = request.session['email']
        now = datetime.now()
        with connection.cursor() as cursor:
            if kategori == 'kesehatan':
                cursor.execute(
                    f'''
                    insert into penggalangan_dana_pd values
                    ('{id}', '{judul}', '{deskripsi}', '{kota}', '{provinsi}', '{berkas}', 'Belum Terverifikasi', '{now}', NULL, '{deadline}', '{targetnominal}', NULL, NULL, NULL, '{email_user}', NULL, '{id_kategori}' );
                    insert into pd_kesehatan values
                    ('{id}', '{penyakit}', '{nik}');
                    '''
                )
            elif kategori == 'rumah ibadah':
                cursor.execute(
                    f'''
                    insert into penggalangan_dana_pd values
                    ('{id}', '{judul}', '{deskripsi}', '{kota}', '{provinsi}', '{berkas}', 'Belum Terverifikasi', '{now}', NULL, '{deadline}', '{targetnominal}', NULL, NULL, NULL, '{email_user}', NULL, '{id_kategori}' );
                    insert into pd_rumah_ibadah values
                    ('{id}', '{nosertif}', '{idaktifitas}');
                    '''
                )
            else:
                cursor.execute(
                    f'''
                    insert into penggalangan_dana_pd values
                    ('{id}', '{judul}', '{deskripsi}', '{kota}', '{provinsi}', '{berkas}', 'Belum Terverifikasi', '{now}', NULL, '{deadline}', '{targetnominal}', NULL, NULL, NULL, '{email_user}', NULL, '{id_kategori}' );
                    '''
                )
        return redirect('list_penggalangan')
    return render(request, 'create_penggalangan.html', response)


def list_penggalangan(request):
    response = {}
    data_penggalangan = []
    data_penggalangan1 = []

    email = request.session['email']

    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT * FROM PENGGALANGAN_DANA_PD
            WHERE email_user = '{email}';
            ''')
        data_penggalangan = cursor.fetchall()
    data_organized = []

    flag = False
    num = 1
    jumlah_aktif = 0
    for i in data_penggalangan:
        if i[9] == "Terverifikasi":
            jumlah_aktif += 1
            flag = True
        temp = (num, i[0], i[1], i[3], i[4], i[8], i[9],
                i[13], i[10], i[16], i[6], flag)
        data_organized.append(temp)
        num += 1

    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT * FROM PENGGALANGAN_DANA_PD;
            ''')
        data_penggalangan1 = cursor.fetchall()
    data_organized1 = []
    flag = True
    num = 1
    for i in data_penggalangan1:
        if i[9] == "Terverifikasi":
            flag = False
        temp = (num, i[0], i[1], i[3], i[4], i[8], i[9],
                i[13], i[10], i[16], i[6], flag)
        data_organized1.append(temp)
        num += 1

    response['data_penggalangan'] = data_organized
    response['data_penggalangan1'] = data_organized1
    response['title'] = 'Data Penggalangan Dana Pribadi'
    response['title1'] = 'Data Penggalangan Dana'
    response['jumlah'] = data_organized.__len__()
    response['aktif'] = jumlah_aktif
    return render(request, 'list_penggalangan.html', response)


def fetch_data_penggalangan(id):
    data = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
                SELECT * from PENGGALANGAN_DANA_PD
                WHERE id = '{id}';
            '''
        )
        data = cursor.fetchone()

    if not data:
        return False

    init_data_utama = {
        'iD_penggalangan_dana': data[0],
        'email_penggalangan_dana': data[14],
        'judul': data[1],
        'deskripsi': data[2],
        'kota': data[3],
        'provinsi': data[4],
        'deadline_penggalangan_dana': data[9],
        'jumlah_target_dana': data[10],
    }
    return init_data_utama


def fetch_data_kesehatan(id):
    data = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
                SELECT * from PD_KESEHATAN PDK JOIN PASIEN ON nik = idpasien 
                NATURAL JOIN KOMORBID JOIN PENGGALANGAN_DANA_PD PD ON PD.id = PDK.idpd
                JOIN KATEGORI_PD KPD ON id_kategori = KPD.id
                WHERE idpd = '{id}';
            '''
        )
        data = cursor.fetchone()

    if not data:
        return False

    terkumpul = 0
    terpakai = 0
    if data[20]:
        terkumpul = data[20]
    if data[21]:
        terpakai = data[21]

    init_tambahan_kesehatan = {
        'kategori': data[27],
        'nIK_pasien': data[3],
        'nama_pasien': data[4],
        'penyakit_utama': data[1],
        'komorbid': data[8],
        'link_berkas_penggalangan_dana': data[14],
        'jumlah_terkumpul': terkumpul,
        'jumlah_terpakai': terpakai

    }
    return init_tambahan_kesehatan


def fetch_data_rumah_ibadah(id):
    data = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
                SELECT * from PD_RUMAH_IBADAH PDRI JOIN RUMAH_IBADAH ON nosertifikat = idrumahibadah
                JOIN kategori_aktivitas_pd_rumah_ibadah on id = idaktivitas 
                JOIN PENGGALANGAN_DANA_PD PD ON PDRI.idpd = PD.id
                JOIN KATEGORI_PD KPD ON id_kategori = KPD.id
                WHERE idpd = '{id}';
            '''
        )
        data = cursor.fetchone()

    if not data:
        return False

    terkumpul = 0
    terpakai = 0
    if data[20]:
        terkumpul = data[20]
    if data[21]:
        terpakai = data[21]

    init_tambahan_rumah_ibadah = {
        'kategori': data[27],
        'nomor_sertifikat_rumah_ibadah': data[3],
        'kategori_aktifitas': data[8],
        'link_berkas_penggalangan_dana': data[14],
        'jumlah_terkumpul': terkumpul,
        'jumlah_terpakai': terpakai
    }
    return init_tambahan_rumah_ibadah


def fetch_data_else(id):
    data = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
                SELECT * from PENGGALANGAN_DANA_PD PD
                JOIN KATEGORI_PD KPD ON id_kategori = KPD.id
                WHERE PD.id = '{id}';
            '''
        )
        data = cursor.fetchone()

    if not data:
        return False

    terkumpul = 0
    terpakai = 0
    if data[11]:
        terkumpul = data[11]
    if data[12]:
        terpakai = data[12]

    init_tambahan_else = {
        'kategori': data[18],
        'link_berkas_penggalangan_dana': data[5],
        'jumlah_terkumpul': terkumpul,
        'jumlah_terpakai': terpakai
    }
    return init_tambahan_else


def detail_penggalangan(request, id):
    response = {}
    data_penggalangan = fetch_data_penggalangan(id)
    tambahan_kesehatan = fetch_data_kesehatan(id)
    tambahan_rumah_ibadah = fetch_data_rumah_ibadah(id)
    tambahan_else = fetch_data_else(id)

    form = DetailPenggalanganDanaForm(
        request.POST or None, initial=data_penggalangan)
    form1 = DetailTambahanPDKesehatanForm(
        request.POST or None, initial=tambahan_kesehatan)
    form2 = DetailTambahanPDRIForm(
        request.POST or None, initial=tambahan_rumah_ibadah)
    form3 = DetailTambahanPDForm(request.POST or None, initial=tambahan_else)

    judul = data_penggalangan['judul']
    response['title'] = 'Detail Penggalangan Dana: ' + judul
    response['form'] = form
    response['form1'] = form1
    response['form2'] = form2
    response['form3'] = form3
    if request.method == 'POST' and form.is_valid():
        return redirect('list_penggalangan')
    return render(request, 'detail_penggalangan.html', response)


def delete_penggalangan(request, kategori, id='noid'):
    with connection.cursor() as cursor:
        if kategori == 'kesehatan':
            cursor.execute(
                f'''
                DELETE FROM PENGGALANGAN_DANA_PD
                WHERE id = '{id}';
                DELETE FROM PD_KESEHATAN
                WHERE idpd = '{id}';
                '''
            )
        elif kategori == 'rumah ibadah':
            cursor.execute(
                f'''
                DELETE FROM PENGGALANGAN_DANA_PD
                WHERE id = '{id}';
                DELETE FROM PD_RUMAH_IBADAH
                WHERE idpd = '{id}';
                '''
            )
        else:
            cursor.execute(
                f'''
                DELETE FROM PENGGALANGAN_DANA_PD
                WHERE id = '{id}';
                '''
            )
        messages.success(request, f'Data Penggalangan Dana berhasil dihapus')
        return redirect('list_penggalangan')
