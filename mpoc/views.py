from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import FileResponse
from django.db.models import Q
from usr.access import restrict_mpoc
from .models import ExecutiveOrder,Ordinance,Incident
from .forms import EOForm,OrdinanceForm,IncidentForm
from django.contrib import messages

# Create your views here.
@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_home(request):
    return render(request,'mpoc.html')


#EXECUTIVE ORDER

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_eo(request):
    eo=ExecutiveOrder.objects.all().order_by('-eo_number')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        eo=ExecutiveOrder.objects.filter(Q(eo_title__icontains=cri)|Q(eo_number__icontains=cri)).order_by('-eo_number')
    return render(request,'mpoc/eo.html',{'eo':eo})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_neweo(request):
    form=EOForm()
    if request.method=='POST':
        try:
            form=EOForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,f"EO Number {request.POST['eo_number']} successfully save.")
        except Exception as e:
            messages.error(request, f'Error : {e}')
        return redirect('mpoc_eo')
    return render(request,'mpoc/neweo.html',{'form':form})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_updateeo(request,pk):
    data=get_object_or_404(ExecutiveOrder,id=pk)
    if request.method=='POST':
        try:
            form=EOForm(request.POST,request.FILES, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,f"EO Number {request.POST['eo_number']} successfully updated.")
        except Exception as e:
            messages.error(request, f'Error : {e}')
        return redirect('mpoc_eo')
    form=EOForm(instance=data)
    return render(request,'mpoc/updateeo.html',{'form':form})


@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_downloadeo(request,pk):
    eo=ExecutiveOrder.objects.get(id=pk)
    if eo.eo_file:
        return FileResponse(eo.eo_file.open('rb'),as_attachment=True)
    else:
        messages.error(request,'No File Found!')
        return redirect('mpoc_eo')
    
@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_deleteeo(request,pk):
    eo=ExecutiveOrder.objects.get(id=pk)
    if eo:
        eo.delete()
        messages.success(request,'Executive Order Deleted!')
        return redirect('mpoc_eo')
    else:
        messages.error(request,'No Data Found!')
        return redirect('mpoc_eo')
    
#ORDINANCE

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_ordinance(request):
    ordinance=Ordinance.objects.all().order_by('-ordinance_number')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        ordinance=Ordinance.objects.filter(Q(ordinance_title__icontains=cri)|Q(ordinance_number__icontains=cri)).order_by('-ordinance_number')
    return render(request,'mpoc/ordinance.html',{'ordinance':ordinance})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_newordinance(request):
    form=OrdinanceForm()
    if request.method=='POST':
        try:
            form=OrdinanceForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,f"Ordinance Number {request.POST['ordinance_number']} successfully save.")
        except Exception as e:
            messages.error(request, f'Error : {e}')
        return redirect('mpoc_ordinance')
    return render(request,'mpoc/newordinance.html',{'form':form})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_updateordinance(request,pk):
    data=get_object_or_404(Ordinance,id=pk)
    if request.method=='POST':
        try:
            form=OrdinanceForm(request.POST,request.FILES, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,f"Ordinance Number {request.POST['ordinance_number']} successfully updated.")
        except Exception as e:
            messages.error(request, f'Error : {e}')
        return redirect('mpoc_ordinance')
    form=OrdinanceForm(instance=data)
    return render(request,'mpoc/updateordinance.html',{'form':form})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_deleteordinance(request,pk):
    ordinance=Ordinance.objects.get(id=pk)
    if ordinance:
        ordinance.delete()
        messages.success(request,'Ordinance Deleted!')
        return redirect('mpoc_ordinance')
    else:
        messages.error(request,'No Data Found!')
        return redirect('mpoc_ordinance')
    
@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_downloadordinance(request,pk):
    ord=Ordinance.objects.get(id=pk)
    if ord.ordinance_file:
        return FileResponse(ord.ordinance_file.open('rb'),as_attachment=True)
    else:
        messages.error(request,'No File Found!')
        return redirect('mpoc_eo')
    

#INCIDENTS

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_incident(request):
    inc=Incident.objects.all().order_by('-incident_number')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        inc=Incident.objects.filter(Q(incident_number__icontains=cri)|Q(crime_category__icontains=cri)).order_by('-incident_number')
    return render(request,'mpoc/incidents/incident.html',{'inc':inc})

def mpoc_newincident(request):
    form=IncidentForm()
    if request.method=='POST':
        try:
            form=IncidentForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,f"Incident Number {request.POST['incident_number']} successfully save.")
        except Exception as e:
            messages.error(request, f'Error : {e}')
        return redirect('mpoc_incident')
    return render(request,'mpoc/incidents/newincident.html',{'form':form})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_updateincidents(request,pk):
    data=get_object_or_404(Incident,id=pk)
    if request.method=='POST':
        try:
            form=IncidentForm(request.POST,request.FILES, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,f"Incident Number {request.POST['incident_number']} successfully updated.")
        except Exception as e:
            messages.error(request, f'Error : {e}')
        return redirect('mpoc_incident')
    form=IncidentForm(instance=data)
    return render(request,'mpoc/incidents/updateincident.html',{'form':form})

@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_downloadincident(request,pk):
    inc=Incident.objects.get(id=pk)
    if inc.incident_file:
        return FileResponse(inc.incident_file.open('rb'),as_attachment=True)
    else:
        messages.error(request,'No File Found!')
        return redirect('mpoc_incident')
    
@login_required
@restrict_mpoc(message='Not Authorized to MPOC Page!',redirect_url='/home')
def mpoc_deleteincident(request,pk):
    incident=Incident.objects.get(id=pk)
    if incident:
        incident.delete()
        messages.success(request,'Incident Deleted!')
        return redirect('mpoc_incident')
    else:
        messages.error(request,'No Data Found!')
        return redirect('mpoc_incident')
    

