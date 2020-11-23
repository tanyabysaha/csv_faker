from celery.result import AsyncResult
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DeleteView, ListView
from django.views.generic.base import View
from mainapp.models import Schema, Column, CeleryTasks
from mainapp.forms import SchemaForm, ColumnFormSet
from mainapp.tasks import create_data_csv


class SchemaList(ListView):
    template_name = 'mainapp/schema_list.html'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaDelete(DeleteView):
    template_name = 'mainapp/schema_delete.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Schema, id=id)

    def get_success_url(self):
        return reverse('schema-list')


class SchemaCreate(View):

    def get(self, *args, **kwargs):
        schema_form = SchemaForm()
        column_form = ColumnFormSet(queryset=Column.objects.none())

        return render(self.request, 'mainapp/schema_create.html',
                      {'schema_form': schema_form, 'column_form': column_form})

    def post(self, *args, **kwargs):
        columns = []
        schema_form = SchemaForm(data=self.request.POST)
        column_form = ColumnFormSet(data=self.request.POST)
        if schema_form.is_valid() and column_form.is_valid():
            schema = schema_form.save(commit=False)
            schema.user = self.request.user
            schema.save()
            schema_title = schema.title
            schema_id = schema.id
            for column in column_form:
                column.save(commit=False)
                column.instance.schema = schema
                column.save()
                columns.append({'name': column.instance.name, 'type': column.instance.type,
                                'order': column.instance.order})

            task = create_data_csv.delay(schema_title, columns, schema_id)
            CeleryTasks.objects.create(task_id=task, schema=schema, user=self.request.user)
            return HttpResponseRedirect(reverse('csv-status'))


class SchemaUpdate(View):

    def get(self, *args, **kwargs):
        schema = Schema.objects.get(id=self.kwargs.get('id'))
        schema_form = SchemaForm(instance=schema)
        column_form = ColumnFormSet(queryset=Column.objects.filter(schema=schema))

        return render(self.request, 'mainapp/schema_edit.html',
                      {'schema_form': schema_form, 'column_form': column_form, })

    def post(self, *args, **kwargs):
        columns = []
        schema = Schema.objects.get(id=self.kwargs.get('id'))
        schema_title = schema.title
        schema_form = SchemaForm(instance=schema, data=self.request.POST)
        column_form = ColumnFormSet(queryset=Column.objects.filter(schema=schema), data=self.request.POST)
        if schema_form.is_valid() and column_form.is_valid():
            schema = schema_form.save()
            for column in column_form:
                column.save(commit=False)
                column.instance.schema = schema
                column.save()
                columns.append({'name': column.instance.name, 'type': column.instance.type,
                                'order': column.instance.order})
            task = create_data_csv.delay(schema_title, columns)
            CeleryTasks.objects.filter(schema=schema).update(task_id=task.id)

            return HttpResponseRedirect(reverse('csv-status'))


class CsvStatus(View):

    def get(self, request):
        tasks = CeleryTasks.objects.filter(user=self.request.user)
        for task in tasks:
            task_result = AsyncResult(task.task_id)
            task.status = task_result.status
            task.save()
            if task.status == 'SUCCESS':
                Schema.objects.filter(id=task.schema.id)

        return render(request, 'mainapp/csv_status.html', {'tasks': tasks})
