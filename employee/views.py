from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from usr.access import ViewEmployee,ViewDtr
from .models import Employee,Department,Biometric
from django.db.models import Q,F,Case,When,Value,CharField
from django.db.models.functions import TruncDate
from datetime import datetime
from django.template.loader import render_to_string
from .functions import punchstate_report,emp_dtr,department_report,emp_lateover,Skiptime,min_hr,chk_punch
from django.http import HttpResponse
from .functions import dtr_functions
import pandas as pd

@login_required()
@user_passes_test(ViewEmployee,login_url='/')
def employee(request):
    return render(request,'employee/employee.html')

@login_required()
@user_passes_test(ViewEmployee,login_url='/')
def employeelist(request):
    data=Employee.objects.all().order_by('employee_id')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Employee.objects.filter(Q(employee_id__icontains=cri)|Q(lastname__icontains=cri)|
                                      Q(firstname__icontains=cri)|Q(middlename__icontains=cri)).order_by('employee_id')
    return render(request,'employee/employee_list.html',{'data':data})

def department_dtr_late_undertime(request,pk):
    data=Employee.objects.all().filter(dept=pk).order_by('type','lastname','firstname')
    dept=Department.objects.all()
    punches=Biometric.objects.all()
    empdf=pd.DataFrame(list(data.values()))
    biodf=pd.DataFrame(list(punches.values()))
    df = pd.merge(empdf, biodf, left_on='biometric_number', right_on='bio_id',  how='left')
    pivot_df=df.pivot_table(index=['dept_id','lastname','firstname','middlename','extname','type','position','bio_id'],columns=('bio_punchstate'),values='bio_time',aggfunc='first')
    required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
    pivot_df = pivot_df.reindex(columns=required_cols, fill_value='').fillna('')
    punch_look=pivot_df.to_dict('index')
    def dname(pk):
        dep=Department.objects.get(id=pk)
        return f'{dep.department}'
    content=[]
    for i,row in pivot_df.iterrows():
        dept=i[0]
        emp=f'{i[1]}, {i[2]} {i[3]} {i[4]}'
        content.append({
            'dept':dname(dept),
            'emp':emp,
            'typ':i[5],
            'cin':Skiptime(punch_look.get('Check In',''),'8:00:00').late()
        })

 
    html=render_to_string('employee/lu_report.html',{'data':data,'df':content})
    return department_report(pk,html)

@login_required()
def Employee_Information(request):
    return render(request,'employee/emp_information.html')

#Time Keeping
@login_required()
def Dtr(request):
    return render(request,'employee/dtr.html')

@login_required()
def Upload_Punches(request):
    return render(request,'employee/upload_punches.html')

@login_required()
def Dtr_Employees(request):
    data=Employee.objects.all().order_by('id')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Employee.objects.filter(Q(biometric_number__icontains=cri)|\
                                     Q(lastname__icontains=cri)|\
                                     Q(firstname__icontains=cri)|\
                                     Q(middlename__icontains=cri)
                                     )
    return render(request,'employee/dtr_employees.html',{'data':data})

@login_required()
def Dtr_Department(request):
    data=Department.objects.all().order_by('department')
    return render(request,'employee/dtr_department.html',{'data':data})

def trunc(request):
    pass

@login_required()
def Dtr_emp_punch_filter(request,pk):
    data=Employee.objects.get(id=pk)
    employee=f'{data.lastname}, {data.firstname} {data.middlename} {data.extname}'
    if request.method=='POST':
        try:
            opt=request.POST
            if opt['opt']=='2':
                bdata=Biometric.objects.filter(bio_id=data.biometric_number,bio_date__range=(opt['startdate'],opt['enddate'])).order_by('bio_date','bio_time')
                emp=Employee.objects.filter(biometric_number=data.biometric_number).first()
                html=render_to_string('employee/punch_report.html',{'data':bdata,'s':opt['startdate'],'e':opt['enddate'],'emp':emp})
                return punchstate_report(pk,html)
            elif opt['opt']=='3':
                content=[]
                a=range(1,32)
                emp=Employee.objects.filter(id=pk).first()
                punches=Biometric.objects.filter(bio_id=data.biometric_number,bio_date__range=(opt['startdate'],opt['enddate'])).values(
                    'bio_date','bio_punchstate','bio_time'
                )
                
                if punches:
                    df=pd.DataFrame(list(punches))
                    df['bio_date']=df['bio_date'].astype(str)
                    pivot_df=df.pivot_table(index='bio_date',columns=('bio_punchstate'),values='bio_time',aggfunc='first')
                    required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                    pivot_df = pivot_df.reindex(columns=required_cols, fill_value='').fillna('')
                    punch_look=pivot_df.to_dict('index')
                t=0
                for i in a:
                        start_dt = datetime.strptime(opt['startdate'], '%Y-%m-%d')
                        start_month = start_dt.month
                        start_year = start_dt.year
                        dyt=dtr_functions(i).loop_date(start_month,start_year)
                        d_data=punch_look.get(dyt,{})

                        cin=Skiptime(d_data.get('Check In',''),'8:00:00').late()
                        bout=Skiptime(d_data.get('Break Out',''),'12:00:00').undertime()
                        bin=Skiptime(d_data.get('Break In',''),'13:00:00').late()  
                        cout=Skiptime(d_data.get('Check Out',''),'17:00:00').undertime()                    

                        total_min=round(cin+bout+bin+cout)
                        hrs=total_min//60
                        minu=total_min%60
                        total_format=f"{hrs}:{minu:02}:00"

                        content.append({
                            'd':dyt,
                            'i':i,  
                            'cin':chk_punch(cin,cout,bin,bout,min_hr(cin)),
                            'bout':chk_punch(cin,cout,bin,bout,min_hr(bout)),  
                            'bin':chk_punch(cin,cout,bin,bout,min_hr(bin)),  
                            'cout':chk_punch(cin,cout,bin,bout,min_hr(cout)),                     
                            'total':total_format if minu> 0 else ''
                            })
                        t+=total_min
                

                html=render_to_string('employee/emp_late_over.html',{'emp':emp,'data':content, 'myr':f'{start_dt.strftime("%B, %Y")}','t':min_hr(t)})
                return emp_lateover(pk,html)
            else:
                content=[]
                a=range(1,32)
                punches=Biometric.objects.filter(bio_id=data.biometric_number,bio_date__range=(opt['startdate'],opt['enddate'])).values(
                    'bio_date','bio_punchstate','bio_time'
                )
                if punches:
                    df=pd.DataFrame(list(punches))
                    df['bio_date']=df['bio_date'].astype(str)
                    pivot_df=df.pivot_table(index='bio_date',columns=('bio_punchstate'),values='bio_time',aggfunc='first')
                    required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                    pivot_df = pivot_df.reindex(columns=required_cols, fill_value='').fillna('')
                    punch_look=pivot_df.to_dict('index')
                for i in a:
                        start_dt = datetime.strptime(opt['startdate'], '%Y-%m-%d')
                        start_month = start_dt.month
                        start_year = start_dt.year
                        dyt=dtr_functions(i).loop_date(start_month,start_year)
                        d_data=punch_look.get(dyt,{})
                        content.append({
                            'd':dyt,
                            'i':i,  
                            'cin':d_data.get('Check In',''),
                            'bout':d_data.get('Break Out',''),  
                            'bin':d_data.get('Break In',''),  
                            'cout':d_data.get('Check Out',''),                     
                            'wday':dtr_functions(i).satsun(start_month,start_year)

                        })
                html=render_to_string('employee/dtr_template.html',{'a':a ,'c':content,'data':employee,'df':pivot_df})
                return emp_dtr(pk,html)
            
        except Exception as e:
            return HttpResponse(e)
            # return render(request,'employee/dtr_emp_punch_filter.html',{'data':data})
    else:
        return render(request,'employee/dtr_emp_punch_filter.html',{'data':data})

@login_required
def department_report_filter(request,pk):
    data=Department.objects.get(id=pk)
    if request.method=='POST':
            criteria=request.POST
            data=Employee.objects.all().filter(dept=pk).order_by('type','lastname','firstname')
            punches=Biometric.objects.all()
            empdf=pd.DataFrame(list(data.values()))
            biodf=pd.DataFrame(list(punches.values()))
            df = pd.merge(empdf, biodf, left_on='biometric_number', right_on='bio_id',  how='left')
            pivot_df=df.pivot_table(index=['dept_id','lastname','firstname','middlename','extname','type','position','bio_id'],columns=('bio_punchstate'),values='bio_time',aggfunc='first')
            required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
            pivot_df = pivot_df.reindex(columns=required_cols, fill_value='').fillna('')
            punch_look=pivot_df.to_dict('index')
            def dname(pk):
                dep=Department.objects.get(id=pk)
                return f'{dep.department}'
            content=[]
            for i,row in pivot_df.iterrows():
                dept=i[0]
                emp=f'{i[1]}, {i[2]} {i[3]} {i[4]}'
                content.append({
                    'dept':dname(dept),
                    'no':i[7],
                    'emp':emp,
                    'typ':i[5],
                    'cin':Skiptime(punch_look.get('Check In',''),'8:00:00').late()
                })

        
            html=render_to_string('employee/lu_report.html',{'data':data,'df':content})
            return department_report(pk,html)

    else:
        return render(request,'employee/dept_hours_filter.html',{'data':data})