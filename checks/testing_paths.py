import os

from django.core.files import File

from models import *


checks = Check.objects.filter(order__id=3000)
for check in checks:
    check.status = 'r'
    # check.pdf_file.path = '/media/3000_client.pdf'
    path = os.path.join(os.getcwd(), 'media/3000_client.pdf')
    with open(path, 'r') as f:
        check.pdf_file = File(f)
        check.save()