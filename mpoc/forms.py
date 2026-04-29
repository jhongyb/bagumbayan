from django import forms
from .models import ExecutiveOrder

class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = ['%Y-%m-%d']

class EOForm(forms.ModelForm):
    class Meta:
        model=ExecutiveOrder
        fields=("eo_date","eo_title","eo_number","eo_file")
        widgets={
            'eo_date':forms.DateInput(attrs={'type':'date'}),}
        labels={
            'eo_date':"Date",
            'eo_number':"Number",
            'eo_title':"Excutive Order Description",
            'eo_file':"Attachment (File)",
            }


