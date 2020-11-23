from io import StringIO
from csv import writer
from django.core.files.base import ContentFile
from faker import Faker
import itertools
from mainapp.models import Schema
from csv_faker.celery import app


@app.task
def create_data_csv(schema, columns, schema_id):
    fake = Faker()
    data_for_csv = {}
    for i in columns:
        if i['type'] == "Full_name":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.name())
        if i['type'] == "Job":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.job())
        if i['type'] == "Email":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.email())
        if i['type'] == "Domain_name":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.domain_name())
        if i['type'] == "Phone_number":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.phone_number())
        if i['type'] == "Company":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.company())
        if i['type'] == "Text":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.text())
        if i['type'] == "Integer":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.random_int())
        if i['type'] == "Address":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.address())
        if i['type'] == "Date":
            for _ in range(i['order']):
                add_or_append(data_for_csv, i['name'], fake.past_date())

    csv_file = StringIO()
    wr = writer(csv_file)
    wr.writerow(data_for_csv.keys())  # writes title row
    for each in itertools.zip_longest(*data_for_csv.values()): wr.writerow(each)
    csv_file = ContentFile(csv_file.getvalue().encode('utf-8'))

    update_schema = Schema.objects.filter(id=schema_id).first()
    update_schema.csv_file.save('{}.csv'.format(schema), csv_file)


def add_or_append(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
