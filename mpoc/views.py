from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import FileResponse
from django.db.models import Q
from usr.access import mpoc_access
from .models import ExecutiveOrder
from .forms import EOForm
from django.contrib import messages

# Create your views here.
@login_required
@user_passes_test(mpoc_access,login_url='/home')
def mpoc_home(request):
    return render(request,'mpoc.html')


@login_required
@user_passes_test(mpoc_access,login_url='/mpoc')
def mpoc_eo(request):
    eo=ExecutiveOrder.objects.all().order_by('-eo_number')
    if request.method=='POST':
        cri=request.POST['txtsearch']
        eo=ExecutiveOrder.objects.filter(Q(eo_title__icontains=cri)|Q(eo_number__icontains=cri)).order_by('-eo_number')
    return render(request,'mpoc/eo.html',{'eo':eo})

@login_required
@user_passes_test(mpoc_access,login_url='/mpoc')
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
@user_passes_test(mpoc_access,login_url='/mpoc')
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
@user_passes_test(mpoc_access,login_url='/home')
def mpoc_downloadeo(request,pk):
    eo=ExecutiveOrder.objects.get(id=pk)
    if eo.eo_file:
        return FileResponse(eo.eo_file.open('rb'),as_attachment=True)
    else:
        messages.error(request,'No File Found!')
        return redirect('mpoc_eo')