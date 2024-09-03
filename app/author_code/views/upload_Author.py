import csv
from io import TextIOWrapper

from author_code.models import Author
from author_code.models import CutterSanbornThreeFigureAuthorTable
from django.shortcuts import render


# Create your views here.

def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        bulk = []
        for line in csv_file:
            AuthorSymbol = CutterSanbornThreeFigureAuthorTable.objects.get(AuthorSymbol=line[0])
            author = Author(Heading=line[1], AuthorSymbol=AuthorSymbol)
            bulk.append(author)

        Author.objects.bulk_create(bulk)

        return render(request, 'author_code/upload_Author.html')

    else:
        return render(request, 'author_code/upload_Author.html')
