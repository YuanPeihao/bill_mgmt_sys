import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Invoice
from common.utils import get_num_of_days_by_month, logger


def render_test(request):
    context = {
        'mylist': ['aaa', 'bbb', 'ccc']
    }
    return render(request, 'bill_collector/test.html', context)


def render_month_selector(request):
    return render(request, 'bill_collector/select_bill_month.html')


def month_selector_bill_middleware(request):
    year, month = map(int, request.GET.get('month').split('-'))
    return HttpResponseRedirect(reverse('bill_collector:monthly_bill', args=(year, month)))


def render_monthly_bill(request, year: int, month: int):
    num_of_days = get_num_of_days_by_month(year, month)
    bill_info = Invoice.get_info_for_monthly_bill(str(year), str(month))
    bill_table = Invoice.convert_bill_info_dict_to_2d_array(bill_info)
    bill_summary = Invoice.bill_info_summary(bill_info)
    context = {
        'year': year,
        'month': month,
        'days': [idx+1 for idx in range(num_of_days)],
        'banks': bill_table[0],
        'bill_table': bill_table,
        'bill_summary': bill_summary
    }
    return render(request, 'bill_collector/month_bill_table.html', context)


@method_decorator(csrf_exempt, name='dispatch')
def add_invoice(request, year: int, month: int):
    body = request.body.decode('utf-8')
    data = Invoice.decorate_data_for_add_ivc(body)
    logger.info('Creating new invoice item, data is {}'.format(data))
    Invoice.objects.create(**data)
    return HttpResponseRedirect(reverse('bill_collector:monthly_bill', args=(year, month)))


@method_decorator(csrf_exempt, name='dispatch')
def delete_invoice(request, year: int, month: int):
    body = request.body.decode('utf-8')
    logger.info('Deleting invoice item, data is {}'.format(body))
    ivc_id = body.split('=')[1]
    ivc = Invoice.objects.get(id=ivc_id)
    res = ivc.delete()
    logger.info('Result is {}'.format(res))
    # need more res handlers here
    return HttpResponseRedirect(reverse('bill_collector:monthly_bill', args=(year, month)))


@method_decorator(csrf_exempt, name='dispatch')
def update_invoice(request, year: int, month: int):
    body = request.body.decode('utf-8')
    data = Invoice.decorate_data_for_add_ivc(body)
    logger.info('Updating invoice item, data is {}'.format(data))
    ivc_to_upd = Invoice.objects.filter(id=data.get('ivc_id'))
    if not ivc_to_upd:
        logger.warning('Invoice ID not found')
    else:
        logger.info('Updating invoice {}'.format(ivc_to_upd))
        data.pop('ivc_id', None)
        ivc_to_upd.update(**data)

    return HttpResponseRedirect(reverse('bill_collector:monthly_bill', args=(year, month)))








