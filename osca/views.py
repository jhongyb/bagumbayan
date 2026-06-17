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
    





