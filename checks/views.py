import os
import json
from base64 import b64encode

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.files import File
from django.http import FileResponse
from django_rq import job

from .models import *


# TODO: Docker-compose
# TODO: Kitchen PDFs have 2 pages instead of 1
# TODO: Proper tests
@job
def render_pdf(json_data):
    url = 'http://172.18.0.3:80'  # Container IP + port
    total = 0
    for item in json_data['items']:
        total += item['quantity'] * item['unit_price']

    # Client printer:
    # TODO: any n of items.
    context = {'id': json_data['id'],
               'address': json_data['address'],
               'client_name': json_data['client']['name'],
               'client_phone': json_data['client']['phone'],
               'item1_name': json_data['items'][0]['name'],
               'item1_quantity': json_data['items'][0]['quantity'],
               'item1_unit_price': json_data['items'][0]['unit_price'],
               'item2_name': json_data['items'][1]['name'],
               'item2_quantity': json_data['items'][1]['quantity'],
               'item2_unit_price': json_data['items'][1]['unit_price'],
               'total': total
               }
    request = None  # It doesn't need the real request.
    response = render(request, 'client_check.html', context=context)
    input_html = response.content
    # To PDF:
    encoding = 'utf-8'
    base64_bytes = b64encode(input_html)
    base64_string = base64_bytes.decode(encoding)
    data0 = {'contents': base64_string,}
    headers = {'Content-Type': 'application/json'}  # This is important
    response = requests.post(url, data=json.dumps(data0), headers=headers)
    # Save the response contents to a file
    with open(f'media/{json_data["id"]}_client.pdf', 'wb') as f:
        f.write(response.content)

    # Kitchen printer:
    response = render(request, 'kitchen_check.html', context=context)
    input_html = response.content
    # To PDF:
    encoding = 'utf-8'
    base64_bytes = b64encode(input_html)
    base64_string = base64_bytes.decode(encoding)
    data0 = {'contents': base64_string}
    headers = {'Content-Type': 'application/json'}  # This is important
    response = requests.post(url, data=json.dumps(data0), headers=headers)
    # Save the response contents to a file
    with open(f'media/{json_data["id"]}_kitchen.pdf', 'wb') as f:
        f.write(response.content)

    # Change check status to "rendered":
    # TODO: files are dead on the server/admin
    checks = Check.objects.filter(order__id=json_data['id'])
    for check in checks:
        check.status = 'r'
        # check.pdf_file.path = '/media/3000_client.pdf'
        path = os.path.join(os.getcwd(), 'media/3000_client.pdf')
        filename = '3000_client.pdf'
        with open(path, 'rb') as f:
            # pass
            check.pdf_file.save(filename, File(f), save=True)
            check.save()

@csrf_exempt  # That way, Django's CSRF middleware will ignore CSRF protection.
def create_checks(request):
    json_data = json.loads(request.body)

    # Select printer with matching point_id:
    point_id = json_data['point_id']
    printers = Printer.objects.filter(point_id=point_id).values('api_key')

    if not printers:
        data = {"error": "NO PRINTERS. Для данной точки не настроено ни одного принтера"}
        return HttpResponse(json.dumps(data), status=400)
    else:
        # Check if checks already exist:
        order_id = json_data['id']
        orders = Check.objects.all().values('order')
        if orders:
            for order in orders:
                if order['order']['id'] == order_id:
                    data = {"error": "ALREADY EXIST. Для данного заказа уже созданы чеки"}
                    return HttpResponse(json.dumps(data), status=400)
    # Kinda else:
    # Create a check for each printer of the point:
    # Select all printers of the point:
    printers = Printer.objects.filter(point_id=point_id)
    for printer in printers:
        c = Check.objects.create(printer=printer, type=printer.check_type,
                                 order=json_data, status="n")
        c.save()
    data = {"ok": "CREATED. Чеки успешно созданы"}
    render_pdf.delay(json_data)
    return HttpResponse(json.dumps(data), status=200)

@csrf_exempt  # That way, Django's CSRF middleware will ignore CSRF protection.
def new_checks(request):
    """Return all rendered checks generated for this printer."""
    api_key = request.GET.get('api_key')
    try:
        p = Printer.objects.get(api_key=api_key)
        checks = Check.objects.filter(printer=p).values('id')
        ids = []
        for check in checks:
            ids.append({'id': check['id']})
        data = {'checks': ids}
        return HttpResponse(json.dumps(data), content_type='application/json',
                            status=200)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "Ошибка авторизации"}),
                            content_type='application/json', status=401)

@csrf_exempt  # That way, Django's CSRF middleware will ignore CSRF protection.
def check(request):
    """Return the PDF for this check."""
    api_key = request.GET.get('api_key')
    check_id = request.GET.get('check_id')
    # Check the printer:
    try:
        p = Printer.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "AUTH: Ошибка авторизации"}),
                            content_type='application/json', status=401)
    # Return PDF:
    try:
        c = Check.objects.get(id=check_id)
        response = FileResponse(open('media/3000_client.pdf', 'rb'), content_type='application/pdf')
        return response
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"error": "No check: Данного чека не существует"}),
                            content_type='application/json', status=400)
