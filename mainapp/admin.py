from django.contrib import admin
from mainapp.models import Schema
from mainapp.models import Column

admin.site.register(Schema)
admin.site.register(Column)