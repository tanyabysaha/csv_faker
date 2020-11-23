from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, IntegerField, ForeignKey, DateTimeField, FileField


class Schema(models.Model):
    title = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=models.CASCADE)
    csv_file = FileField(null=True)


class Column(models.Model):
    TYPE_CHOICES = [
        ('Full_name', 'Full name'),
        ('Job', 'Job'),
        ('Email', 'Email'),
        ('Domain_name', 'Domain name'),
        ('Phone_number', 'Phone number'),
        ('Company', 'Company'),
        ('Text', 'Text'),
        ('Integer', 'Integer'),
        ('Address', 'Address'),
        ('Date', 'Date'),
    ]
    schema = ForeignKey('Schema', on_delete=models.CASCADE)
    name = CharField(max_length=255, blank=True, null=True)
    type = CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True)
    order = IntegerField(blank=True, null=True)
    range_from = IntegerField(blank=True, null=True)
    range_to = IntegerField(blank=True, null=True)


class CeleryTasks(models.Model):
    schema = ForeignKey('Schema', on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)
    status = CharField(max_length=255, blank=True, null=True)
    task_id = CharField(max_length=255, blank=True, null=True)
