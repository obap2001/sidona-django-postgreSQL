
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection, InternalError, reset_queries
from .forms import adminRegisterForm, penggalangRegisterForm, individuRegisterForm, organisasiRegisterForm
from login.views import login

# Register Admin


def registerAdmin(request):
    # response for Passing data into Templates
    response = {}

    # Institiate The Form
    form = adminRegisterForm(request.POST or None)

    # Assigning data for response
    response['form'] = form
    response['title'] = 'Register Admin'

    # generating id
    existing_id = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id_pegawai From sidona.ADMIN;'
        )
        existing_id = cursor.fetchall()

    last_id = 0
    for id in existing_id:
        if last_id < int(id[0]):
            last_id = int(id[0])

    # Getting data from Form on POST
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        nama = form.cleaned_data['nama']
        noHP = form.cleaned_data['nomorHP']
        idPegawai = str(last_id+1)

        # Execute Query for Registering
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''
                    insert into sidona.akun_pengguna values
                    ('{email}', '{password}', 'ADMIN', '{nama}');
                    insert into sidona.admin values
                    ('{email}','{password}' ,'{nama}', '{noHP}', '{idPegawai}');
                    '''
                )
                messages.success(
                    request, 'Berhasil terdaftar sebagai admin!')
                login(request, email, password)
                return redirect('home')

            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to siruco;
                    SELECT nama FROM ADMIN
                    WHERE email='{email}';'''
                )
                data = cursor.fetchone()
                if data:  # Exception if user already register
                    messages.error(
                        request, 'Maaf, email yang anda gunakan sudah terdaftar! Gunakan email yang lain.')

    return render(request, 'register.html', response)


def registerPenggalang(request):
    response = {}
    form = penggalangRegisterForm(request.POST or None)
    response['form'] = form
    response['title'] = 'Register Penggalang Dana'

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        nama = form.cleaned_data['nama']
        alamat = form.cleaned_data['alamat']
        noHP = form.cleaned_data['noHP']
        namaBank = form.cleaned_data['namaBank']
        jenis = form.cleaned_data['jenis']
        norek = form.cleaned_data['noRekening']

        # Execute Querry
        with connection.cursor() as cursor:
            try:
                if jenis == 'INDIVIDU':
                    cursor.execute(
                        f'''
                        insert into akun_pengguna values
                        ('{email}', '{password}', 'PENGGALANG DANA', '{nama}');
                        insert into penggalang_dana values
                        ('{email}','{password}' ,'{nama}','{noHP}','{alamat}', 0, '{norek}', '{namaBank}', '{None}', 0, 0, 'Belum verifikasi', 'fszantho0@mozilla.org');
                        '''
                    )
                    return redirect('individu', email, password)
                elif jenis == 'ORGANISASI':
                    cursor.execute(
                        f'''
                        insert into akun_pengguna values
                        ('{email}', '{password}', 'PENGGALANG DANA', '{nama}');
                        insert into penggalang_dana values
                        ('{email}','{password}' ,'{nama}','{noHP}','{alamat}', 0, '{norek}', '{namaBank}', '{None}', 0, 0, 'Belum verifikasi', 'fszantho0@mozilla.org');
                        '''
                    )
                    return redirect('organisasi', email, password)
            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to sidona;
                    SELECT nama FROM penggalang_dana
                    WHERE USERNAME='{email}';'''
                )
                data = cursor.fetchone()
                if data:  # Exception if user already register
                    messages.error(
                        request, 'Maaf, email yang anda gunakan sudah tedaftar.')

    return render(request, 'register.html', response)


def registerIndividu(request, email, password):
    response = {}
    form = individuRegisterForm(request.POST or None)

    response['title'] = 'Pendaftaran Penggalang Dana Individu'
    response['form'] = form

    if request.method == 'POST' and form.is_valid():
        nik = form.cleaned_data['nik']
        tglLahir = form.cleaned_data['tglLahir']
        jenisKelamin = form.cleaned_data['jenisKelamin']
        link = form.cleaned_data['linkfotoKTP']
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''
                    insert into individu values
                    ('{email}', '{nik}', '{tglLahir}', '{jenisKelamin}', 0);
                    update penggalang_dana set link_repo = '{link}'
                    where email = '{email}';
                '''
                )
                messages.success(
                    request, 'Berhasil terdaftar sebagai Penggalang Dana Individu')
                login(request, email, password)
                return redirect('home')
            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to sidona;
                    SELECT nama FROM penggalang_dana
                    WHERE USERNAME='{email}';'''
                )
                data = cursor.fetchone()
                if data:  # Exception if user already register
                    messages.error(
                        request, 'Maaf, email yang anda gunakan sudah tedaftar.')

    return render(request, 'individu.html', response)


def registerOrganisasi(request, email, password):
    response = {}
    form = organisasiRegisterForm(request.POST or None)

    response['title'] = 'Pendaftaran Penggalang Dana Organisasi'
    response['form'] = form

    if request.method == 'POST' and form.is_valid():
        noakta = form.cleaned_data['noAkta']
        namaorg = form.cleaned_data['namaOrang']
        notelp = form.cleaned_data['notelp']
        tahun = form.cleaned_data['tahunBerdiri']
        link = form.cleaned_data['linkFotoAkta']

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f'''
                    insert into organisasi values
                    ('{email}', '{noakta}', '{namaorg}', '{notelp}', '{tahun}');
                    update penggalang_dana set link_repo = '{link}'
                    where email = '{email}';
                '''
                )
                messages.success(
                    request, 'Berhasil terdaftar sebagai Penggalang Dana Organisasi')
                login(request, email, password)
                return redirect('home')
            except InternalError:
                # Check if user already regitstered or not
                cursor.execute(
                    f'''set search_path to sidona;
                    SELECT nama FROM penggalang_dana
                    WHERE USERNAME='{email}';'''
                )
                data = cursor.fetchone()
                if data:  # Exception if user already register
                    messages.error(
                        request, 'Maaf, email yang anda gunakan sudah tedaftar.')

    return render(request, 'organisasi.html', response)
