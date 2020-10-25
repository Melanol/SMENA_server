from django.db import models
from django.contrib.postgres.fields import JSONField


class Printer(models.Model):
    name = models.CharField(max_length=20)
    api_key = models.CharField(max_length=20, unique=True)
    check_type = models.CharField(max_length=20,
                                  choices=(('k', 'kitchen'),
                                           ('c', 'client')))
    point_id = models.IntegerField()

    def __str__(self):
        return f"name: {self.name}; api_key: {self.api_key}; " \
               f"check_type: {self.get_check_type_display()}; " \
               f"point_id: {self.point_id}"


class Check(models.Model):
    printer = models.ForeignKey(Printer, models.PROTECT)
    type = models.CharField(max_length=20, choices=(('k', 'kitchen'),
                                                    ('c', 'client')))
    order = JSONField()
    status = models.CharField(max_length=20,
                              choices=(('n', 'new'),
                                       ('r', 'rendered'),
                                       ('p', 'printed')))
    pdf_file = models.FileField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return f"printer_id: {self.printer}; type: {self.type}; " \
               f"status: {self.get_status_display()}"
