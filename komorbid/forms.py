from datetime import date
from uuid import NAMESPACE_DNS
from django.core.exceptions import ValidationError
import re
from django import forms
from django.db import connection
from django.forms import widgets
from django.forms.widgets import Textarea, URLInput

from django.utils.formats import date_format


def fetch_data_pd():
    data_pd = []
    with connection.cursor() as cursor:
        cursor.execute(
            f'''SELECT idpd From sidona.PD_Kesehatan 
            join penggalangan_dana_pd on id = idpd ;'''
        )
        data_pd = cursor.fetchall()
    data_organized = []
    for i in data_pd:
        temp = (i[0], f'{i[0]}')
        data_organized.append(temp)
    return tuple(data_organized)


class CreateKomorbidForm(forms.Form):
    idpd = forms.ChoiceField(choices=fetch_data_pd(),
                             label='ID Penggalangan Dana Kesehatan')
    komorbid = forms.CharField(max_length=50, label='Komorbid')
