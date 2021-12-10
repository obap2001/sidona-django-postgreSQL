
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection, InternalError
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
    form1 = individuRegisterForm(request.POST or None)
    form2 = organisasiRegisterForm(request.POST or None)
    response['form'] = form
    response['form1'] = form1
    response['form2'] = form2
    response['title'] = 'Register Penggalang Dana'
    response['title1'] = 'Register Penggalang Dana Individu'
    response['title2'] = 'Register Penggalang Dana Organisasi'
    if request.method == 'POST' and form.is_valid() and (form1.is_valid() or form2.is_valid()):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        nama = form.cleaned_data['nama']
        alamat = form.cleaned_data['alamat']
        noHP = form.cleaned_data['noHP']
        namaBank = form.cleaned_data['namaBank']
        jenis = form.cleaned_data['jenis']
        norek = form.cleaned_data['noRekening']
        if jenis == 'INDIVIDU':
            nik = form1.cleaned_data['nik']
            tglLahir = form1.cleaned_data['tglLahir']
            jenisKelamin = form1.cleaned_data['jenisKelamin']
            linkKTP = form1.cleaned_data['linkfotoKTP']
        elif jenis == 'ORGANISASI':
            namaorg = form2.cleaned_data['namaOrganisasi']
            noAkta = form2.cleaned_data['noAkta']
            noTelp = form2.cleaned_data['noAkta']
            tahun = form2.cleaned_data['noAkta']
            linkAkta = form2.cleaned_data['noAkta']

        # Execute Querry
        with connection.cursor() as cursor:
            try:
                if jenis == 'INDIVIDU':
                    cursor.execute(
                        f'''
                        insert into akun_pengguna values
                        ('{email}', '{password}', 'PENGGALANG DANA', '{nama}');
                        insert into penggalang_dana values
                        ('{email}','{password}' ,'{nama}','{noHP}','{alamat}', 0, '{norek}', '{namaBank}', '{linkKTP}', 0, 0, 'Belum verifikasi', 'fszantho0@mozilla.org');
                        insert into individu values
                        ('{email}', '{nik}', '{tglLahir}', '{jenisKelamin}', 0);
                        '''
                    )
                elif jenis == 'ORGANISASI':
                    cursor.execute(
                        f'''
                        insert into akun_pengguna values
                        ('{email}', '{password}', 'PENGGALANG DANA', '{nama}');
                        insert into penggalang_dana values
                        ('{email}','{password}' ,'{nama}','{noHP}','{alamat}', 0, '{norek}', '{namaBank}', '{linkAkta}', 0, 0, 'Belum verifikasi', 'fszantho0@mozilla.org');
                        insert into organisasi values
                        ('{email}', '{noAkta}', '{namaorg}', '{noTelp}', '{tahun}');
                        '''
                    )
                messages.success(
                    request, 'Berhasil terdaftar sebagai Penggalang Dana')
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

    return render(request, 'register.html', response)
