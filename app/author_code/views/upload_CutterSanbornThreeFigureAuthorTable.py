import csv
from io import TextIOWrapper

from author_code.models import CutterSanbornThreeFigureAuthorTable
from django.shortcuts import render


# Create your views here.

def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        bulk = []
        for line in csv_file:
            authorsymbol = CutterSanbornThreeFigureAuthorTable(AuthorSymbol=line[0], AuthorName=line[1])
            bulk.append(authorsymbol)

        CutterSanbornThreeFigureAuthorTable.objects.bulk_create(bulk)

        return render(request, 'author_code/upload_CutterSanbornThreeFigureAuthorTable.html')

    else:
        return render(request, 'author_code/upload_CutterSanbornThreeFigureAuthorTable.html')
