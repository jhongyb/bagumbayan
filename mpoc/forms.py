from django import forms
from .models import ExecutiveOrder,Ordinance,Incident

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

class OrdinanceForm(forms.ModelForm):
    class Meta:
        model=Ordinance
        fields=("ordinance_date","ordinance_title","ordinance_number","ordinance_file")
        widgets={
            'ordinance_date':forms.DateInput(attrs={'type':'date'}),}
        labels={
            'ordinance_date':"Date",
            'ordinance_number':"Number",
            'ordinance_title':"Ordinance Description",
            'ordinance_file':"Attachment (File)",
            }

class IncidentForm(forms.ModelForm):
    class Meta:
        model=Incident
        fields=("incident_number","barangay","purok","incident_type","crime_category",
                "incident_datetime","date_reported","status","action_taken","narrative","incident_file")
        widgets={
            'incident_datetime':forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'date_reported':forms.DateTimeInput(attrs={'type':'datetime-local'}),}
        labels={

            }
