
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from usr.access import restrict_osca
from .forms import OscaForm
from django.contrib import messages
from .models import Osca_Informations
from django.db.models import Q

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def osca(request):

    return render(request,'osca.html')

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def newosca(request):
    form=OscaForm()
    if request.method=='POST':
            form=OscaForm(request.POST)
            if form.is_valid():
                 form.save()
                 messages.success(request,'Data successfully Added')
                 pass    
    return render(request,'osca/newsenior.html',{'form':form})

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def oscamasterlist(request):
    data=Osca_Informations.objects.all().order_by("idno")
    if request.method=='POST':
         cri=request.POST['txtsearch']
         data=Osca_Informations.objects.filter(Q(idno__icontains=cri)|Q(lastname__icontains=cri)|
                                               Q(firstname__icontains=cri)|Q(middlename__icontains=cri)|
                                               Q(purok__icontains=cri)|Q(barangay__barangay_name__icontains=cri)
                                               ).order_by("idno")
    return render(request,'osca/seniorlist.html',{'data':data})

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def updatesenior(request,pk):
    data=get_object_or_404(Osca_Informations,id=pk)
    if request.method=='POST':
            form=OscaForm(request.POST,instance=data)
            if form.is_valid():
                 form.save()
                 messages.success(request,'Data successfully Updated')
                 pass
    form=OscaForm(instance=data)    
    return render(request,'osca/updatesenior.html',{'form':form})

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def deletesenior(request,pk):
    eo=Osca_Informations.objects.get(id=pk)
    if eo:
        eo.delete()
        messages.success(request,'Senior Citizen Deleted!')
        return redirect('oscamasterlist')
    else:
        messages.error(request,'Something Error!')
        return redirect('oscamasterlist')
    





from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse
from usr.access import restrict_osca
from .forms import OscaForm
from django.contrib import messages
from .models import Osca_Informations
from django.db.models import Q,Value,Count
from django.db import IntegrityError
from django.db.models.functions import Coalesce
from .reports import OscaReports, Senior_Report
from django.template.loader import render_to_string

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def osca(request):

    return render(request,'osca.html')

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def newosca(request):
    if request.method=='POST':
        form = OscaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Data successfully Added')
                return redirect('oscamasterlist')
            except IntegrityError as e:
                messages.error(request, f'Database Error: {e}')
                pass
        else:
            # This triggers if form.is_valid() fails (e.g., duplicate data caught by Django)
            for field, errors in form.errors.items():
                for error in errors:
                    # Strips the field name prefix if it's a non-field error
                    error_msg = f"{field.title()}: {error}" if field != '__all__' else error
                    messages.error(request, error_msg)
            
            pass
            
    else:
        form = OscaForm()
    return render(request, 'osca/newsenior.html', {'form': form})

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def oscamasterlist(request):
    data=Osca_Informations.objects.all().order_by("idno")[:100]
    if request.method=='POST':
         cri=request.POST['txtsearch']
         data=Osca_Informations.objects.filter(Q(idno__icontains=cri)|Q(lastname__icontains=cri)|
                                               Q(firstname__icontains=cri)|Q(middlename__icontains=cri)|
                                               Q(purok__icontains=cri)|Q(barangay__barangay_name__icontains=cri)
                                               ).order_by("idno")[:50]
    return render(request,'osca/seniorlist.html',{'data':data})

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def updatesenior(request,pk):
    data=get_object_or_404(Osca_Informations,id=pk)
    if request.method=='POST':
            form=OscaForm(request.POST,instance=data)
            if form.is_valid():
                 form.save()
                 messages.success(request,'Data successfully Updated')
                 pass
    form=OscaForm(instance=data)    
    return render(request,'osca/updatesenior.html',{'form':form})

@login_required()
@restrict_osca(message='Not Authorized to OSCA Page!',redirect_url='/home')
def deletesenior(request,pk):
    eo=Osca_Informations.objects.get(id=pk)
    if eo:
        eo.delete()
        messages.success(request,'Senior Citizen Deleted!')
        return redirect('oscamasterlist')
    else:
        messages.error(request,'Something Error!')
        return redirect('oscamasterlist')
    
def oscabarangayfigure(request):
    count=Osca_Informations.objects.annotate(brgy=Coalesce('barangay__barangay_name',Value('')))\
                        .values('brgy','barangay').annotate(
                            male=Count("id",filter=Q(sex='M')),
                            female=Count("id",filter=Q(sex='F')),
                            total=Count('id')).order_by('brgy')
    tcount=Osca_Informations.objects.count()
    return render(request,'osca/seniorbarangayfigure.html',{'count':count,'tcount':tcount})

#REPORTS
def Senior_All(request):
    data=OscaReports().All_list()
    html=render_to_string('osca/pdf_senior_all.html',{'data':data})
    return Senior_Report(html).A4('landscape')

def Senior_listby_barangay(request,pk):
    data=OscaReports().Senior_listby_barangay(pk)
    html=render_to_string('osca/pdf_senior_all.html',{'data':data})
    return Senior_Report(html).A4('landscape')

def Senior_Figures(request):
    data=OscaReports().All_Barangay_Figure()
    html=render_to_string('osca/pdf_senior_figures.html',{'data':data})
    return Senior_Report(html).A4('portrait')

def Senior_Figures_barangay(request,pk):
    data=OscaReports().Barangay_Figure_filter(pk)
    html=render_to_string('osca/pdf_senior_figures.html',{'data':data})
    return Senior_Report(html).A4('portrait')

def senior_80above(request):
    data=OscaReports().listof80
    html=render_to_string('osca/pdf_senior_all.html',{'data':data,'title':'AGE OF 80 AND ABOVED'})
    return Senior_Report(html).A4('landscape')



