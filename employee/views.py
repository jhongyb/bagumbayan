from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from usr.access import restrict_employee
from .models import Employee,Department,Biometric
from django.db.models import Q,F,Case,When,Value,CharField
from django.db.models.functions import TruncDate
from datetime import datetime
from django.template.loader import render_to_string
from .functions import punchstate_report,emp_dtr,department_report,emp_lateover,Skiptime,min_hr,Late_Undertime
from django.http import HttpResponse
from .functions import dtr_functions
import pandas as pd
from datetime import datetime
from django.contrib import messages
import calendar


@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def employee(request):
    return render(request,'humanresource.html')

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def employeelist(request):
    data=Employee.objects.all().order_by('lastname','firstname')
    try:
        if request.method=='POST':
            cri=request.POST['txtsearch']
            data=Employee.objects.filter(Q(employee_id__icontains=cri)|Q(lastname__icontains=cri)|
                                        Q(firstname__icontains=cri)|Q(middlename__icontains=cri)).order_by('employee_id')
            return render(request,'employee/employee_list.html',{'data':data})
    except Exception as e:
        messages.error(request,e)
    return render(request,'employee/employee_list.html',{'data':data})

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def department_dtr_late_undertime(request,pk):
    try:
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
    except Exception as e:
         messages.error(request,e)
    html=render_to_string('employee/lu_report.html',{'data':data,'df':content})
    return department_report(pk,html)

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def Employee_Information(request):
    return render(request,'employee/emp_information.html')

#Time Keeping
@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def Dtr(request):
    return render(request,'employee/dtr.html')
@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def Upload_Punches(request):
    return render(request,'employee/upload_punches.html')

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def Dtr_Employees(request):
    data=Employee.objects.all().order_by('lastname','firstname')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Employee.objects.filter(Q(biometric_number__icontains=cri)|\
                                     Q(lastname__icontains=cri)|\
                                     Q(firstname__icontains=cri)|\
                                     Q(middlename__icontains=cri)
                                     )
    return render(request,'employee/dtr_employees.html',{'data':data})

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def Dtr_Department(request):
    data=Department.objects.all().order_by('department')
    return render(request,'employee/dtr_department.html',{'data':data})

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def Dtr_emp_punch_filter(request,pk):
    data=Employee.objects.get(id=pk)
    employee=f' {data.firstname} {data.middlename} {data.lastname} {data.extname}'
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
                        
                        cin=Late_Undertime("CI",d_data.get('Check In',''),d_data.get('Break Out',''),d_data.get('Break In',''),d_data.get('Check Out','')).checkin()
                        bout=Late_Undertime("BO",d_data.get('Check In',''),d_data.get('Break Out',''),d_data.get('Break In',''),d_data.get('Check Out','')).breakout()  
                        bin=Late_Undertime("BI",d_data.get('Check In',''),d_data.get('Break Out',''),d_data.get('Break In',''),d_data.get('Check Out','')).breakin()  
                        cout=Late_Undertime("CO",d_data.get('Check In',''),d_data.get('Break Out',''),d_data.get('Break In',''),d_data.get('Check Out','')).checkout()
                        total_min=round(cin+bout+bin+cout)
                        hrs=total_min//60
                        minu=total_min % 60
                        total_format=f"{hrs}:{minu:02}:00"

                        content.append({
                            'd':dyt,
                            'i':i,  
                            'cin':min_hr(cin),
                            'bout':min_hr(bout),  
                            'bin':min_hr(bin),  
                            'cout':min_hr(cout),                     
                            'total':total_format if minu> 0 else '',
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
                else:
                     messages.error(request,f'NO DATA FOUND!')
                
                for i in a:
                        start_dt = datetime.strptime(opt['startdate'], '%Y-%m-%d')
                        my=start_dt.strftime("%B %Y")
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
                html=render_to_string('employee/dtr_template.html',{'a':a ,'c':content,'data':employee,'df':pivot_df,'my':my})
                return emp_dtr(pk,html)
            
        except Exception as e:
             messages.error(request,e)
        return render(request,'employee/dtr_emp_punch_filter.html',{'data':data})
    else:
        return render(request,'employee/dtr_emp_punch_filter.html',{'data':data})
    
@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/employee')
def department_report_filter(request,pk):
        dpt=Department.objects.get(id=pk)

        if request.method=='POST':
                data=request.POST
                option=data['opt']
                date_start=data['startdate']
                date_end=data['enddate']
                emp_typ=data['emptype']
                if option=='2':
                    result=[]
                    emp=Employee.objects.all().filter(dept=pk,type=emp_typ).order_by('type','lastname','firstname')
                    punches=Biometric.objects.filter(bio_date__range=(date_start,date_end))
                    empdf=pd.DataFrame(list(emp.values()))
                    print(pd.col)
                    biodf=pd.DataFrame(list(punches.values()))
                    df = pd.merge(empdf, biodf, left_on='biometric_number', right_on='bio_id',  how='left')
                    df['bio_date']=df['bio_date'].astype(str)
                    if punches:
                        pivot_df=df.pivot_table(index=('bio_date','biometric_number','dept_id','lastname','firstname','middlename','extname','type'),columns=('bio_punchstate'),values='bio_time',aggfunc='first')
                        required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                        pivot_df = pivot_df.reindex(columns=required_cols, fill_value='').fillna('')
                    else:
                         messages.error(request,'No Data Found!')
                         return redirect('department_report_filter')
                        
                    flat_df = pivot_df.reset_index()
                    # 2. Calculate CIN and COUT for each individual row
                    def calculate_cin(row):
                        return Late_Undertime("CI", row['Check In'], row['Break Out'], row['Break In'], row['Check Out']).checkin()

                    def calculate_cout(row):
                        return Late_Undertime("CO", row['Check In'], row['Break Out'], row['Break In'], row['Check Out']).checkout()
                    flat_df['CIN'] = flat_df.apply(calculate_cin, axis=1)
                    flat_df['COUT'] = flat_df.apply(calculate_cout, axis=1)
                    # 3. Create a unique Employee Identifier/Name string
                    flat_df['emp_name'] = flat_df.apply(
                        lambda r: f"{r['lastname']}, {r['firstname']} {r['middlename']} {r['extname']}".strip(), 
                        axis=1
                    )
                    # 4. Group by Employee and SUM the CIN and COUT columns
                    summary_df = flat_df.groupby(['emp_name', 'type'], as_index=False)[['CIN', 'COUT']].sum()
                    summary_df = summary_df.sort_values(by=['type', 'emp_name'], ascending=[True, True])

                    # 5. Convert the final aggregated dataframe to your desired list of dicts format
                    for _, row in summary_df.iterrows():
                            total_min=round(row['CIN'] + row['COUT'])
                            days = total_min // 480 
                            remaining_min_after_days = total_min % 480
                            # 2. Calculate Hours from the remaining minutes
                            hrs = remaining_min_after_days // 60
                            # 3. Calculate Minutes from what's left over
                            minu = remaining_min_after_days % 60
                            # 4. Format your final output string
                            total_format = f"Days: {days} | Hours: {hrs} | Minutes: {minu:02}"
                            result.append({
                                'emp': row['emp_name'].upper(),
                                'dept':dpt.description,
                                'typ': row['type'],
                                'CIN': min_hr(row['CIN']),
                                'COUT': min_hr(row['COUT']),
                                'TOTAL':total_format if total_min > 0 else '',
                            })
                    html=render_to_string('employee/lu_report.html',{'res':result,'dept':dpt,'sd':datetime.strptime(date_start,'%Y-%m-%d').strftime('%B %d, %Y'),'ed':
                                                                    datetime.strptime(date_end,'%Y-%m-%d').strftime('%B %d, %Y')})
                    return department_report(pk,html)  
                else:
                    employee=Employee.objects.filter(dept=dpt,type=emp_typ)
                    allempdtr=[]
                    start_dt = datetime.strptime(date_start, '%Y-%m-%d')
                    my=start_dt.strftime("%B %Y")
                    start_month = start_dt.month
                    start_year = start_dt.year                    
                    _, total_days = calendar.monthrange(start_year, start_month)
 
                    allempdtr = []
                    for emp in employee:
                        biometric = Biometric.objects.filter(bio_id=emp.biometric_number, bio_date__range=(date_start, date_end))
                        if biometric.exists():
                             df = pd.DataFrame(list(biometric.values('bio_date', 'bio_punchstate', 'bio_time')))
                             df['bio_date'] = df['bio_date'].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else str(x))
                             pivot_df = df.pivot_table(index='bio_date', columns='bio_punchstate', values='bio_time', aggfunc='first')
                             r_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                             r_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                             pivot_df = pivot_df.reindex(columns=r_cols, fill_value='')
                             punch_look = pivot_df.to_dict('index')
                        else:
                            punch_look = {}
                        emp_content=[]
                        for i in range(1,total_days + 1):
                            dyt=dtr_functions(i).loop_date(start_month,start_year)
                            d_data=punch_look.get(dyt,{})
                            emp_content.append({
                                    'd':dyt,
                                    'i':i,  
                                    'cin':d_data.get('Check In',''),
                                    'bout':d_data.get('Break Out',''),  
                                    'bin':d_data.get('Break In',''),  
                                    'cout':d_data.get('Check Out',''),                     
                                    'wday':dtr_functions(i).satsun(start_month,start_year)

                            })
                        allempdtr.append({
                                'emp_info':emp,'dtr_rows':emp_content
                            })
                    context={'emp':allempdtr,'my':my}
                    html=render_to_string('employee/deptdtr_template.html',context)
                    return emp_dtr(dpt,html)
        else:
            return render(request,'employee/dept_hours_filter.html',{'dpt':dpt})


           
                