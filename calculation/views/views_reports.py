'''
  -----------     Reports    ----------------------
'''


from datetime import date, datetime

from django.conf import settings
from django.views.generic import View
from django.views.generic import TemplateView
from django.utils import dateformat
from django.shortcuts import get_object_or_404

from ..models import Invoice
from ..service.calculations import get_report_calculation_of_day
from ..service.calculations import get_report_product_accounting
from ..service.calculations import save_report_to_excel
from ..service.render import Render



class InvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['invoice'] = get_object_or_404(Invoice, pk=kwargs['pk'])
        return Render.render('reports/report_invoice.html', context)

class CalculationXlsView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        if(kwargs):
            date_now = date(int(kwargs['year']),
                            int(kwargs['month']),
                            int(kwargs['day']))
            return save_report_to_excel(date_now, int(kwargs['childrens']))
        else:
            context['date_now'] = datetime.now().date()
            context['childrens'] = 250
            return Render.render('reports/report_calculation.html', context)


class CalculationPdfView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        if(kwargs):
            date_now = date(int(kwargs['year']),
                            int(kwargs['month']),
                            int(kwargs['day']))
            context['date_now'] = dateformat.format(date_now,
                                                    settings.DATE_FORMAT)
            context.update(get_report_calculation_of_day(
                date_now,
                int(kwargs['childrens'])))
        else:
            context['date_now'] = datetime.now().date()
            context['childrens'] = 250
        return Render.render('reports/report_calculation.html', context)


class CalculationView(TemplateView):

    template_name = 'list/calculations.html'

    def get_context_data(self, **kwargs):
        context = super(CalculationView, self).get_context_data(**kwargs)
        if(kwargs):
            context['date_now'] = date(int(kwargs['year']),
                                       int(kwargs['month']),
                                       int(kwargs['day']))
            context.update(get_report_calculation_of_day(
                context['date_now'],
                int(kwargs['childrens'])))
        else:
            context['date_now'] = datetime.now().date()
            context['childrens'] = 250
        return context


class ReportProductAccounting(TemplateView):

    template_name = 'report_pa.html'

    def get_context_data(self, **kwargs):
        context = super(ReportProductAccounting, self).\
            get_context_data(**kwargs)
        if kwargs:
            period = {'from': date(int(kwargs['from_year']),
                                   int(kwargs['from_month']),
                                   int(kwargs['from_day'])),
                      'to': date(int(kwargs['to_year']),
                                 int(kwargs['to_month']),
                                 int(kwargs['to_day']))}
            context.update(get_report_product_accounting(period))
        return context
