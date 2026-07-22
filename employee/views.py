from django.shortcuts import render,redirect,get_object_or_404
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
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
def employee(request):
    return render(request,'humanresource.html')

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
def employeelist(request):
    data=Employee.objects.all().order_by('lastname','firstname')
    try:
        if request.method=='POST':
            cri=request.POST['txtsearch']
            data=Employee.objects.filter(Q(employee_id__icontains=cri)|Q(lastname__icontains=cri)|
                                        Q(firstname__icontains=cri)|Q(middlename__icontains=cri)
                                        |Q(dept__department__icontains=cri)).order_by('employee_id')
            return render(request,'employeehome_list.html',{'data':data})
    except Exception as e:
        messages.error(request,e)
    return render(request,'employee/employee_list.html',{'data':data})

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
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
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
def Employee_Information(request):
    return render(request,'employee/emp_information.html')

#Time Keeping
@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
def Dtr(request):
    return render(request,'employee/dtr.html')
@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
def Upload_Punches(request):
    return render(request,'employee/upload_punches.html')

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
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
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
def Dtr_Department(request):
    data=Department.objects.all().order_by('department')
    return render(request,'employee/dtr_department.html',{'data':data})

@login_required()
@restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
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
    
# @login_required()
# @restrict_employee(message='Not Authorized to Human Resource Page!',redirect_url='/home')
# def department_report_filter(request,pk):
#         dpt=Department.objects.get(id=pk)

#         if request.method=='POST':
#                 data=request.POST
#                 option=data['opt']
#                 date_start=data['startdate']
#                 date_end=data['enddate']
#                 emp_typ=data['emptype']
#                 if option == '2':
#                     result = []
#                     emp = Employee.objects.filter(dept=pk, type=emp_typ).order_by('type', 'lastname', 'firstname')
#                     punches = Biometric.objects.filter(bio_date__range=(date_start, date_end))

#                     # Convert QuerySets to DataFrames
#                     empdf = pd.DataFrame(list(emp.values()))
                    
#                     if empdf.empty:
#                         messages.error(request, 'No Employees Found!')
#                         return redirect('department_report_filter')

#                     # Construct standard employee name column
#                     empdf['emp_name'] = empdf.apply(
#                         lambda r: f"{r['lastname']}, {r['firstname']} {r['middlename']} {r['extname']}".strip(), 
#                         axis=1
#                     )

#                     biodf = pd.DataFrame(list(punches.values()))

#                     # Process Biometrics if logs exist
#                     if not biodf.empty:
#                         df = pd.merge(empdf, biodf, left_on='biometric_number', right_on='bio_id', how='inner')
#                         df['bio_date'] = df['bio_date'].astype(str)

#                         pivot_df = df.pivot_table(
#                             index=('bio_date', 'biometric_number', 'emp_name', 'type'),
#                             columns=('bio_punchstate'),
#                             values='bio_time',
#                             aggfunc='first'
#                         )
                        
#                         required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
#                         pivot_df = pivot_df.reindex(columns=required_cols, fill_value='').fillna('')
#                         flat_df = pivot_df.reset_index()

#                         # Calculate CIN and COUT
#                         flat_df['CIN'] = flat_df.apply(
#                             lambda r: Late_Undertime("CI", r['Check In'], r['Break Out'], r['Break In'], r['Check Out']).checkin(), 
#                             axis=1
#                         )
#                         flat_df['COUT'] = flat_df.apply(
#                             lambda r: Late_Undertime("CO", r['Check In'], r['Break Out'], r['Break In'], r['Check Out']).checkout(), 
#                             axis=1
#                         )

#                         # Group by employee to sum up CIN and COUT values
#                         summary_df = flat_df.groupby(['biometric_number', 'emp_name', 'type'], as_index=False)[['CIN', 'COUT']].sum()

#                         # Merge calculations back into the main employee DataFrame so ALL employees remain
#                         final_df = pd.merge(empdf[['biometric_number', 'emp_name', 'type']], summary_df, on=['biometric_number', 'emp_name', 'type'], how='left')
#                         final_df[['CIN', 'COUT']] = final_df[['CIN', 'COUT']].fillna(0)
#                     else:
#                         # If no biometric logs exist at all, initialize default 0 totals for everyone
#                         final_df = empdf[['emp_name', 'type']].copy()
#                         final_df['CIN'] = 0.0
#                         final_df['COUT'] = 0.0

#                     final_df = final_df.sort_values(by=['type', 'emp_name'], ascending=[True, True])

#                     # Convert aggregated dataframe to template dict list
#                     for _, row in final_df.iterrows():
#                         total_min = round(row['CIN'] + row['COUT'])
#                         days = total_min // 480 
#                         remaining_min_after_days = total_min % 480
#                         hrs = remaining_min_after_days // 60
#                         minu = remaining_min_after_days % 60
                        
#                         total_format = f"Days: {days} | Hours: {hrs} | Minutes: {minu:02}"
                        
#                         result.append({
#                             'emp': row['emp_name'].upper(),
#                             'dept': dpt.description,
#                             'typ': row['type'],
#                             'CIN': min_hr(row['CIN']) if row['CIN'] > 0 else '',
#                             'COUT': min_hr(row['COUT']) if row['COUT'] > 0 else '',
#                             'TOTAL': total_format if total_min > 0 else '',
#                         })

#                     html = render_to_string('employee/lu_report.html', {
#                         'res': result,
#                         'dept': dpt,
#                         'sd': datetime.strptime(date_start, '%Y-%m-%d').strftime('%B %d, %Y'),
#                         'ed': datetime.strptime(date_end, '%Y-%m-%d').strftime('%B %d, %Y')
#                     })
#                 return department_report(pk, html)
#         return render(request,'employee/dept_hours_filter.html',{'dpt':dpt})

def department_report_filter(request, pk):
    dpt = get_object_or_404(Department, id=pk)
    if request.method == 'POST':
        data = request.POST
        option = data.get('opt')
        date_start = data.get('startdate')
        date_end = data.get('enddate')
        emp_typ = data.get('emptype')

        if option == '2':
            result = []
            emp = Employee.objects.filter(dept=pk, type=emp_typ).order_by('type', 'lastname', 'firstname')
            
            # 1. Handle empty employee list immediately
            if not emp.exists():
                messages.error(request, 'No Employees Found!')
                return redirect('department_report_filter', pk=pk)

            # Convert employees to DataFrame safely
            empdf = pd.DataFrame(list(emp.values()))

            # Safely handle potential None/NaN values in name fields
            for col in ['lastname', 'firstname', 'middlename', 'extname']:
                if col in empdf.columns:
                    empdf[col] = empdf[col].fillna('')
                else:
                    empdf[col] = ''

            empdf['emp_name'] = empdf.apply(
                lambda r: f"{r['lastname']}, {r['firstname']} {r['middlename']} {r['extname']}".strip(), 
                axis=1
            )

            # Query biometrics filtered by date range
            punches = Biometric.objects.filter(bio_date__range=(date_start, date_end))
            biodf = pd.DataFrame(list(punches.values())) if punches.exists() else pd.DataFrame()

            # Process Biometrics if logs exist
            if not biodf.empty and 'biometric_number' in empdf.columns:
                df = pd.merge(empdf, biodf, left_on='biometric_number', right_on='bio_id', how='inner')
                
                if not df.empty:
                    df['bio_date'] = df['bio_date'].astype(str)

                    pivot_df = df.pivot_table(
                        index=['bio_date', 'biometric_number', 'emp_name', 'type'],
                        columns=['bio_punchstate'],
                        values='bio_time',
                        aggfunc='first'
                    )
                    
                    required_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                    # Reindex columns safely to guarantee required columns exist
                    pivot_df = pivot_df.reindex(columns=required_cols).fillna('')
                    flat_df = pivot_df.reset_index()

                    # Calculate CIN and COUT
                    flat_df['CIN'] = flat_df.apply(
                        lambda r: Late_Undertime("CI", r.get('Check In', ''), r.get('Break Out', ''), r.get('Break In', ''), r.get('Check Out', '')).checkin(), 
                        axis=1
                    )
                    flat_df['COUT'] = flat_df.apply(
                        lambda r: Late_Undertime("CO", r.get('Check In', ''), r.get('Break Out', ''), r.get('Break In', ''), r.get('Check Out', '')).checkout(), 
                        axis=1
                    )

                    # Group by employee to sum up CIN and COUT values
                    summary_df = flat_df.groupby(['biometric_number', 'emp_name', 'type'], as_index=False)[['CIN', 'COUT']].sum()

                    # Merge back so ALL employees are retained
                    final_df = pd.merge(
                        empdf[['biometric_number', 'emp_name', 'type']], 
                        summary_df, 
                        on=['biometric_number', 'emp_name', 'type'], 
                        how='left'
                    )
                    final_df[['CIN', 'COUT']] = final_df[['CIN', 'COUT']].fillna(0)
                else:
                    final_df = empdf[['emp_name', 'type']].copy()
                    final_df['CIN'] = 0.0
                    final_df['COUT'] = 0.0
            else:
                # If no biometric logs exist at all
                final_df = empdf[['emp_name', 'type']].copy()
                final_df['CIN'] = 0.0
                final_df['COUT'] = 0.0

            final_df = final_df.sort_values(by=['type', 'emp_name'], ascending=[True, True])

            # Convert aggregated dataframe to template list
            for _, row in final_df.iterrows():
                cin_val = row.get('CIN', 0)
                cout_val = row.get('COUT', 0)
                total_min = round(cin_val + cout_val)
                
                days = total_min // 480 
                remaining_min_after_days = total_min % 480
                hrs = remaining_min_after_days // 60
                minu = remaining_min_after_days % 60
                
                total_format = f"Days: {days} | Hours: {hrs} | Minutes: {minu:02}"
                
                result.append({
                    'emp': str(row['emp_name']).upper(),
                    'dept': dpt.description,
                    'typ': row['type'],
                    'CIN': min_hr(cin_val) if cin_val > 0 else '',
                    'COUT': min_hr(cout_val) if cout_val > 0 else '',
                    'TOTAL': total_format if total_min > 0 else '',
                })

            html = render_to_string('employee/lu_report.html', {
                'res': result,
                'dept': dpt,
                'sd': datetime.strptime(date_start, '%Y-%m-%d').strftime('%B %d, %Y'),
                'ed': datetime.strptime(date_end, '%Y-%m-%d').strftime('%B %d, %Y')
            })
            return department_report(pk, html)

        else:
                    # employee=Employee.objects.filter(dept=dpt,type=emp_typ)
                    # allempdtr=[]
                    # start_dt = datetime.strptime(date_start, '%Y-%m-%d')
                    # my=start_dt.strftime("%B %Y")
                    # start_month = start_dt.month
                    # start_year = start_dt.year                    
                    # _, total_days = calendar.monthrange(start_year, start_month)
 
                    # allempdtr = []
                    # for emp in employee:
                    #     biometric = Biometric.objects.filter(bio_id=emp.biometric_number, bio_date__range=(date_start, date_end))
                    #     if biometric.exists():
                    #          df = pd.DataFrame(list(biometric.values('bio_date', 'bio_punchstate', 'bio_time')))
                    #          df['bio_date'] = df['bio_date'].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else str(x))
                    #          pivot_df = df.pivot_table(index='bio_date', columns='bio_punchstate', values='bio_time', aggfunc='first')
                    #          r_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                    #          r_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                    #          pivot_df = pivot_df.reindex(columns=r_cols, fill_value='')
                    #          punch_look = pivot_df.to_dict('index')
                    #     else:
                    #         punch_look = {}
                    #     emp_content=[]
                    #     for i in range(1,total_days + 1):
                    #         dyt=dtr_functions(i).loop_date(start_month,start_year)
                    #         d_data=punch_look.get(dyt,{})
                    #         emp_content.append({
                    #                 'd':dyt,
                    #                 'i':i,  
                    #                 'cin':d_data.get('Check In',''),
                    #                 'bout':d_data.get('Break Out',''),  
                    #                 'bin':d_data.get('Break In',''),  
                    #                 'cout':d_data.get('Check Out',''),                     
                    #                 'wday':dtr_functions(i).satsun(start_month,start_year)

                    #         })
                    #     allempdtr.append({
                    #             'emp_info':emp,'dtr_rows':emp_content
                    #         })
                    # context={'emp':allempdtr,'my':my}
                    # html=render_to_string('employee/deptdtr_template.html',context)
                    # return emp_dtr(dpt,html)

                employee = Employee.objects.filter(dept=dpt, type=emp_typ)
                allempdtr = []
                start_dt = datetime.strptime(date_start, '%Y-%m-%d')
                my = start_dt.strftime("%B %Y")
                start_month = start_dt.month
                start_year = start_dt.year                    
                _, actual_days = calendar.monthrange(start_year, start_month)

                allempdtr = []
                for emp in employee:
                    biometric = Biometric.objects.filter(bio_id=emp.biometric_number, bio_date__range=(date_start, date_end))
                    if biometric.exists():
                        df = pd.DataFrame(list(biometric.values('bio_date', 'bio_punchstate', 'bio_time')))
                        df['bio_date'] = df['bio_date'].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else str(x))
                        
                        # Avoid redundant duplicate definition of r_cols
                        r_cols = ['Check In', 'Break Out', 'Break In', 'Check Out']
                        pivot_df = df.pivot_table(index='bio_date', columns='bio_punchstate', values='bio_time', aggfunc='first')
                        pivot_df = pivot_df.reindex(columns=r_cols, fill_value='')
                        punch_look = pivot_df.to_dict('index')
                    else:
                        punch_look = {}

                    emp_content = []
                    
                    # Always loop 31 days to ensure a complete 31-row DTR
                    for i in range(1, 32):
                        if i <= actual_days:
                            # Valid calendar date
                            dyt = dtr_functions(i).loop_date(start_month, start_year)
                            wday = dtr_functions(i).satsun(start_month, start_year)
                            d_data = punch_look.get(dyt, {})
                        else:
                            # Blank values for padding days beyond the end of the month
                            dyt = ''
                            wday = ''
                            d_data = {}

                        emp_content.append({
                            'd': dyt,
                            'i': i,  
                            'cin': d_data.get('Check In', ''),
                            'bout': d_data.get('Break Out', ''),  
                            'bin': d_data.get('Break In', ''),  
                            'cout': d_data.get('Check Out', ''),                     
                            'wday': wday
                        })

                    allempdtr.append({
                        'emp_info': emp,
                        'dtr_rows': emp_content
                    })

                context = {'emp': allempdtr, 'my': my}
                html = render_to_string('employee/deptdtr_template.html', context)
                return emp_dtr(dpt, html)
    return render(request, 'employee/dept_hours_filter.html', {'dpt': dpt})


         
                