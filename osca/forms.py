from django import forms
from .models import Osca_Informations


class OscaForm(forms.ModelForm):
    class Meta:
        model=Osca_Informations
        fields=("__all__")
        widgets={
            'birthday':forms.DateInput(attrs={'type':'date'}),
            'date_issued':forms.DateInput(attrs={'type':'date'}),
            }
        labels={
            'idno':"ID Number",
            'lastname':"Last Name",
            'firstname':"First Name",
            'middlename':"Middle Name",
            'extname':"Ext Name",
            'birthday':"Birthday",
            'date_issued':"Date Issue",
            'member_status':"Member Status",
        }

