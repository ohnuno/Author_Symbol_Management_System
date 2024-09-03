import csv
from io import TextIOWrapper

from django.db.utils import IntegrityError

from author_code.models import SubjectCode
from django.shortcuts import render


# Create your views here.

def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        bulk = []
        for line in csv_file:
            subjectcode = SubjectCode(SubjectCode=line[0], Language=line[1])
            bulk.append(subjectcode)

        try:
            SubjectCode.objects.bulk_create(bulk, ignore_conflicts=True)
        except IntegrityError:
            for item in bulk:
                SubjectCode.objects.update_or_create(item)

        return render(request, 'author_code/upload_SubjectCode.html')

    else:
        return render(request, 'author_code/upload_SubjectCode.html')
