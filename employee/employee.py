from .models import Employee
from .forms import EmployeeForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages

def newemployee(request):
    
    if request.method=='POST':
        form=EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Data successfully save.')
            return redirect('employeelist')
    else:
        form=EmployeeForm()
    context={'form':form}
    return render(request,'employee/emp/newemployee.html',context)


def updateemployee(request,pk):
    data=get_object_or_404(Employee,pk=pk)
    if request.method=='POST':
        form=EmployeeForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Data successfully save.')
            return redirect('updateemployee',pk=pk)
    else:
        form=EmployeeForm(instance=data)
    context={'form':form}
    return render(request,'employee/emp/update_employee.html',context)