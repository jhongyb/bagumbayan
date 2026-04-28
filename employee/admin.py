from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget,DateWidget
from import_export.admin import ImportExportModelAdmin
from .models import Department, Employee, Biometric
from rangefilter.filters import DateRangeFilter

class BiometricResource(resources.ModelResource):
    bio_date = fields.Field(
        column_name='bio_date',
        attribute='bio_date',
        widget=DateWidget(format='%Y-%m-%d')
    )
    class Meta:
        model = Biometric
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('bio_id', 'bio_date', 'bio_time')
        
    

@admin.register(Biometric)
class BiometricAdmin(ImportExportModelAdmin):
    resource_class = BiometricResource
    # 'get_emp_name' and 'bio_id_number' are the methods defined below
    list_display = ('get_emp_name', 'bio_id_number', 'bio_date', 'bio_time', 'bio_punchstate')
    list_filter = ('bio_date', 'bio_punchstate', 'bio_id')
    list_editable=('bio_date', 'bio_punchstate', 'bio_time')
    search_fields = ('bio_id',)
    list_filter=(('bio_date',DateRangeFilter),('bio_id'))

    # Helper method to show Employee Name in the list
    def get_emp_name(self, obj):
        emp = Employee.objects.filter(biometric_number=obj.bio_id).first()
        return f"{emp.lastname}, {emp.firstname} {emp.middlename}" if emp else "Unknown"
    get_emp_name.short_description = 'Employee Name'

    # Helper method to show the Biometric Number in the list
    def bio_id_number(self, obj):
        return obj.bio_id
    bio_id_number.short_description = 'Bio ID'

# 1. Resource mapping for Employee
class EmployeeResource(resources.ModelResource):
    # column_name: What the CSV header says
    # attribute: The field name in your Employee model (dept)
    # widget: Points to Department model and its unique field 'department'
    dept = fields.Field(
        column_name='department',
        attribute='dept',
        widget=ForeignKeyWidget(Department, 'department') 
    )

    class Meta:
        model = Employee
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        fields = (
            'id', 'biometric_number', 'employee_id', 'lastname', 
            'firstname', 'middlename', 'extname', 'birthday', 
            'sex', 'dept', 'position', 'type'
        )
        # Use biometric_number to identify existing records and prevent duplicates
        import_id_fields = ('biometric_number',)

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = [
        'lastname', 'firstname', 'middlename', 'dept', 
        'biometric_number', 'employee_id', 'type'
    ]
    search_fields = ['lastname', 'firstname', 'biometric_number']
    list_filter = ['dept', 'sex', 'type']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department', 'description']

admin.site.site_header='ICT ADMIN PAGE'
