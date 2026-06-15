
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
from django.contrib import messages


def parse_time(time_str):
          if not time_str:
               return None
          try:
               return datetime.strptime(time_str, "%H:%M:%S").time()
          except ValueError:
               return None 

class Skiptime:
     def __init__(self,punch,typ):
          self.p=punch
          self.s=typ
          self.today=date.today()


     def lateundertime(self,cin=None,bout=None,bin=None,cout=None):
            if self.p:
               #LATE
                 if self.s=='CI' and self.p > parse_time("08:00:00"):
                    p_dt=datetime.combine(self.today,cin)
                    s_dt=datetime.combine(self.today,parse_time("08:00:00"))
                    total_seconds=p_dt-s_dt
                    
                 elif self.s=='BI' and self.p > parse_time("13:00:00"):
                    p_dt=datetime.combine(self.today,self.p)
                    s_dt=datetime.combine(self.today,parse_time("13:00:00"))
                    total_seconds=p_dt-s_dt
               # UNDERTIME REVERSE FUNCTION 
                 elif self.s=='BO' and bout==None:
                    return 0

                 elif self.s=='CO' and self.p < parse_time("17:00:00"):
                    s_dt=datetime.combine(self.today,bout if bout!=None else bin)
                    p_dt=datetime.combine(self.today,parse_time("17:00:00"))
                    total_seconds=p_dt-s_dt          
                 else:
                         return 0
                 return total_seconds.total_seconds()/60
            
          #NOT PUNCH
            else:   
               if self.s=='CI' and bout or bin:
                    p_dt=datetime.combine(self.today,bout or bin)
                    s_dt=datetime.combine(self.today,parse_time("08:00:00"))
               if self.s=='CO' and bout or bin:
                    s_dt=datetime.combine(self.today,bout or bin)
                    p_dt=datetime.combine(self.today,parse_time("17:00:00"))
               else:
                         return 0
               
               total_seconds=p_dt-s_dt
               return total_seconds.total_seconds()/60
                
     def punch_skip(self):
          pass
def min_hr(m):
    total_minutes = int(round(m))
    if total_minutes>0:
          hours = total_minutes // 60
          minutes = total_minutes % 60
          return f"{hours}:{minutes:02}:00"
    else:
         return ''
class Late_Undertime:
     def __init__(self,status,cin,bout,bin,cout):
          self.cin=cin
          self.bout=bout
          self.bin=bin
          self.cout=cout
          self.status=status
          self.today=date.today()
     def checkin(self):
          if self.status=='CI':
               if self.cin and self.cin > parse_time("08:00:00"):
                    p_dt=datetime.combine(self.today,self.cin)
                    s_dt=datetime.combine(self.today,parse_time("08:00:00"))
               elif not self.cin and self.bout:
                    p_dt=datetime.combine(self.today,self.bout)
                    s_dt=datetime.combine(self.today,parse_time("08:00:00"))
               elif not self.cin and not self.bout and self.bin:
                    p_dt=datetime.combine(self.today,self.bin)
                    s_dt=datetime.combine(self.today,parse_time("08:00:00"))
               elif not self.cin and not self.bout and not self.bin and self.cout:
                    p_dt=datetime.combine(self.today,self.cout)
                    s_dt=datetime.combine(self.today,parse_time("08:00:00"))
               else:
                    return 0
          total_seconds=p_dt-s_dt
          return total_seconds.total_seconds()//60
     def checkout(self):
          if self.status=='CO':
               if self.cout and self.cout < parse_time("17:00:00"):
                    s_dt=datetime.combine(self.today,self.cout)
                    p_dt=datetime.combine(self.today,parse_time("17:00:00"))
               elif  not self.cout and self.bout:
                    s_dt=datetime.combine(self.today,self.bout)
                    p_dt=datetime.combine(self.today,parse_time("17:00:00"))
               elif  not self.cout and not self.bout and not self.bin and self.cin:
                    s_dt=datetime.combine(self.today,self.cin)
                    p_dt=datetime.combine(self.today,parse_time("17:00:00"))
               else:
                    return 0
          total_seconds=p_dt-s_dt
          return total_seconds.total_seconds()//60
     def breakin(self):
          if self.status=='BI':
               if self.bin and self.bin > parse_time("13:00:00"):
                    p_dt=datetime.combine(self.today,self.bin)
                    s_dt=datetime.combine(self.today,parse_time("13:00:00"))
               elif not self.bin and self.cout:
                    p_dt=datetime.combine(self.today,parse_time("13:00:00"))
                    s_dt=datetime.combine(self.today,parse_time("13:00:00"))
               else:
                    return 0
               
          total_seconds=p_dt-s_dt
          return total_seconds.total_seconds()//60
     
     def breakout(self):
          if self.status=='BO':
               if self.bout and self.bout < parse_time("12:00:00"):
                    s_dt=datetime.combine(self.today,self.bin)
                    p_dt=datetime.combine(self.today,parse_time("12:00:00"))
               elif not self.bout:
                    s_dt=datetime.combine(self.today,parse_time("13:00:00"))
                    p_dt=datetime.combine(self.today,parse_time("13:00:00"))
               else:
                    return 0
               
          total_seconds=p_dt-s_dt
          return total_seconds.total_seconds()//60


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
       config =pdfkit.configuration(wkhtmltopdf='./static/wkhtmltopdf') 
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
            'margin-bottom': '0.5in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'title':"DTR",
            'footer-Font-size':'8',
       }
       config =pdfkit.configuration(wkhtmltopdf='./static/wkhtmltopdf') 
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
            'footer-left':'© YB IT SOLUTIONS',
            'footer-Font-size':'4',
       }
       config =pdfkit.configuration(wkhtmltopdf='./static/wkhtmltopdf') 
       pdf = pdfkit.from_string(html, False, configuration=config, 
       options=options)
       response = HttpResponse(pdf, content_type='application/pdf')
       response['Content-Disposition'] = 'inline; filename="'+f"DTR : {aydi}.pdf".format('Report','12')
       return response


class dtr_functions:
     def __init__(self,days):
          self.day=days
     def loop_date(self,m,y):
          try:
               return f"{y}-{str(m).zfill(2)}-{str(self.day).zfill(2)}"
          except:
               return ''
     
     def aydi(self,a):
          return f"{a}"
     
     def satsun(self,m,y):
          try:
               dyt=datetime.date(datetime.strptime(self.loop_date(m,y),'%Y-%m-%d'))
               if dyt.weekday()==5:
                    return 'SATURDAY'
               elif dyt.weekday()==6:
                    return 'SUNDAY'
               else:
                    return ''
          except:
               return ''
def department_report(iid,html):
       try:
          aydi=iid
          html=html
          options = {
               'page-size': 'A4',
               'orientation':'portrait',
               'encoding': "UTF-8",
               'margin-top': '0.5in',
               'margin-right': '0.2in',
               'margin-bottom': '0.5in',
               'margin-left': '0.2in',
               'encoding': "UTF-8",
               'print-media-type':'',
               'enable-local-file-access': True,
               'footer-right':'Page  [PAGE] of [topage]',
               'footer-left':'© YB IT SOLUTIONS',
               'title':"PUNCH STATE",
               'footer-Font-size':'4',
               'no-outline':None,
          }
          config =pdfkit.configuration(wkhtmltopdf='./static/wkhtmltopdf') 
          pdf = pdfkit.from_string(html, False, configuration=config, 
          options=options)
          response = HttpResponse(pdf, content_type='application/pdf')
          response['Content-Disposition'] = 'inline; filename="'+f"{aydi}.pdf".format('Report','12')
          return response
       except Exception as e:
            pass
            