
import pdfkit
from django.db.models import F,Q,Sum,Func,CharField,IntegerField
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime,time,date


def parse_time(time_str):
    # Check if the string is empty before parsing
          if not time_str:
               return None
          try:
               return datetime.strptime(time_str, "%H:%M:%S").time()
          except ValueError:
               return None # Or handle incorrectly formatted strings

class Skiptime:
     def __init__(self,punch,schedule):
          self.p=punch
          self.s=parse_time(schedule)
          self.today=date.today()
     
     def late(self):
            if self.p:
                 if self.p> self.s:
                    p_dt=datetime.combine(self.today,self.p)
                    s_dt=datetime.combine(self.today,self.s)
                    total_seconds=p_dt-s_dt
                    return total_seconds.total_seconds()/60
                 else:
                      return 0
            else:
                 return 0
            
     def undertime(self):
            if self.p:
                 if self.p<self.s:
                    p_dt=datetime.combine(self.today,self.p)
                    s_dt=datetime.combine(self.today,self.s)
                    total_seconds=s_dt-p_dt
                    return total_seconds.total_seconds()/60
                 else:
                      return 0
            else:
                 return 0
def min_hr(m):
    total_minutes = int(round(m))
    if total_minutes>0:
          hours = total_minutes // 60
          minutes = total_minutes % 60
          return f"{hours}:{minutes:02}:00"
    else:
         return ''
def chk_punch(cin,cout,bin,bout,status):
     ct='-' if cin>=0 else cin
     l=[]
     l.append((ct,cout,bin,bout))
     if status:
          return status
     else:
          if len(l)>0:
               return "-"

          

def punchstate_report(iid,html):
       aydi=iid
       html=html
       options = {
          'page-width': '4in',
          'page-height': '13in',
          'orientation':'portrait',
          'encoding': "UTF-8",
            'margin-top': '0.5in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'title':"PUNCH STATE",
            'footer-Font-size':'8',}
       config =pdfkit.configuration(wkhtmltopdf='.\static\wkhtmltopdf.exe') 
       pdf = pdfkit.from_string(html, False, configuration=config, 
       options=options)
       response = HttpResponse(pdf, content_type='application/pdf')
       response['Content-Disposition'] = 'inline; filename="'+f"{aydi}.pdf".format('Report','12')
       return response

def strpform(sd):
        if sd:
            try:
                return int(datetime.strptime(sd,'%d/%m/%Y').strftime('%d'))
            except:
                return int(datetime.strptime(sd,'%Y-%m-%d').strftime('%d'))
        else:
             return ''
          
def stime(sd):
        if sd:
            try:
                return datetime.strptime(sd,'%H:%M:%S').strftime('%I:%M')
            except:
                return datetime.strptime(sd,'%H:%M').strftime('%I:%M')
        else:
             return ''   

def emp_dtr(iid,html):
       aydi=iid
       html=html
       options = {
         'page-width': '3.5in',
         'page-height': '8.5in',
          'orientation':'portrait',
          'encoding': "UTF-8",
            'margin-top': '0.3in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'title':"DTR",
            'footer-Font-size':'8',
       }
       config =pdfkit.configuration(wkhtmltopdf='.\static\wkhtmltopdf.exe') 
       pdf = pdfkit.from_string(html, False, configuration=config, 
       options=options)
       response = HttpResponse(pdf, content_type='application/pdf')
       response['Content-Disposition'] = 'inline; filename="'+f"DTR : {aydi}.pdf".format('Report','12')
       return response

def emp_lateover(iid,html):
       aydi=iid
       html=html
       options = {
         'page-width': '3.5in',
         'page-height': '8.5in',
          'orientation':'portrait',
          'encoding': "UTF-8",
            'margin-top': '0.3in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'title':"LATE/UNDERTIME",
            'footer-Font-size':'8',
       }
       config =pdfkit.configuration(wkhtmltopdf='.\static\wkhtmltopdf.exe') 
       pdf = pdfkit.from_string(html, False, configuration=config, 
       options=options)
       response = HttpResponse(pdf, content_type='application/pdf')
       response['Content-Disposition'] = 'inline; filename="'+f"DTR : {aydi}.pdf".format('Report','12')
       return response


class dtr_functions:
     def __init__(self,days):
          self.day=days
     def loop_date(self,m,y):
          return f"{y}-{str(m).zfill(2)}-{str(self.day).zfill(2)}"
     
     def satsun(self,m,y):
          dyt=datetime.date(datetime.strptime(self.loop_date(m,y),'%Y-%m-%d'))
          if dyt.weekday()==5:
               return 'SATURDAY'
          elif dyt.weekday()==6:
               return 'SUNDAY'
          else:
               return ''
def department_report(iid,html):
       aydi=iid
       html=html
       options = {
          'page-size': 'A4',
          'orientation':'landscape',
          'encoding': "UTF-8",
            'margin-top': '0.5in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'title':"PUNCH STATE",
            'footer-Font-size':'8',
       }
       config =pdfkit.configuration(wkhtmltopdf='.\static\wkhtmltopdf.exe') 
       pdf = pdfkit.from_string(html, False, configuration=config, 
       options=options)
       response = HttpResponse(pdf, content_type='application/pdf')
       response['Content-Disposition'] = 'inline; filename="'+f"{aydi}.pdf".format('Report','12')
       return response