from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import connection
from .forms import loginForm

# Create your views here.


def login_view(request):
    if 'email' in request.session:  # Check if user logged in or not
        return redirect('home')

    else:
        response = {}
        form = loginForm(request.POST or None)
        response['form'] = form
        response['title'] = 'Register Penggalang Dana'

        if request.method == 'POST' and form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            login(request, email, password)
            if not 'email' in request.session:
                messages.error(request, 'Data pengguna tidak ditemukan')

        if 'email' in request.session:
            return redirect('home')
        else:
            return render(request, 'login.html', response)


def login(request, username, password):
    data = None
    with connection.cursor() as cursor:
        cursor.execute(
            f'''set search_path to sidona;
            SELECT email, role, nama FROM akun_pengguna 
            WHERE email='{username}' AND PASSWORD='{password}';'''
        )
        data = cursor.fetchone()

    if data:
        request.session['email'] = data[0]
        request.session['peran'] = data[1]
        request.session['nama'] = data[2]
        messages.success(request, f'Berhasil log in sebagai {data[1]}')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Anda sudah logged out!')
    return redirect('home')
