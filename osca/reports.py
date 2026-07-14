from .models import Osca_Informations
import pdfkit
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import ExpressionWrapper, F, IntegerField
from django.db.models.functions import ExtractDay
from django.db.models import Q,Value,Count
from django.db import IntegrityError
from django.db.models.functions import Coalesce


class OscaReports:
    def __init__(self):
        today = timezone.now().date()
        self.data = Osca_Informations.objects.annotate(
            age=ExpressionWrapper(
                ExtractDay(today - F('birthday')) / 365.25,
                output_field=IntegerField()
            )
        ).filter(member_status='A')
    def All_list(self):
        data=self.data
        return data.order_by('barangay','lastname','firstname')
    def Senior_listby_barangay(self,bpk):
        data=self.data.filter(barangay=bpk)
        return data
    def All_Barangay_Figure(self):
        data=self.data.annotate(brgy=Coalesce('barangay__barangay_name',Value('')))\
                        .values('brgy','status__status_description',
                                'category__category_description').annotate(
                                    M=Count('id',filter=Q(sex='M')),
                                    F=Count('id',filter=Q(sex='F')),
                                    total=Count('id')).order_by('brgy')
        return data
    def Barangay_Figure_filter(self,bpk):
        data=self.data.annotate(brgy=Coalesce('barangay__barangay_name',Value('')))\
                        .values('brgy','status__status_description',
                                'category__category_description').annotate(
                                    M=Count('id',filter=Q(sex='M')),
                                    F=Count('id',filter=Q(sex='F')),
                                    total=Count('id')).order_by('brgy').filter(barangay=bpk)
        return data

    def listof80(self):
        data=self.data.filter(age__gte=80)
        return data


class Senior_Report:
    def __init__(self, html):
        self.html = html
    def A4(self,orientation):
        try:
            options = {
                'page-size': 'A4',
                'orientation': orientation,
                'encoding': "UTF-8",
                'margin-top': '0.5in',
                'margin-right': '0.2in',
                'margin-bottom': '0.5in',
                'margin-left': '0.2in',
                'print-media-type': '',
                'enable-local-file-access': True,
                'footer-right': 'Page  [PAGE] of [topage]',
                'footer-left': '© YB IT SOLUTIONS',
                'title': "OSCA",
                'footer-Font-size': '4',
                'no-outline': None,
            }
            config = pdfkit.configuration(wkhtmltopdf='.\static\wkhtmltopdf.exe') 
            pdf = pdfkit.from_string(self.html, False, configuration=config, options=options)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="OSCA_REPORT.pdf"'
            return response

        except Exception as e:
            return HttpResponse(f"An error occurred while generating the PDF: {e}")
        

