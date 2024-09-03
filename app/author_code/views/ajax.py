from author_code.models import Author, AuthorSymbol, Work
from author_code.tasks import merge, recalculation, bulk_create_works
from widgets.author_code import author_table_query, bulk_create
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
import pandas as pd
import io


def ajax_authorsymbol_search(request):
    keyword = request.GET.get('keyword')
    symbol_list = []
    print(keyword)
    if keyword:
        result = author_table_query.query(keyword)
        items = Author.objects.filter(
            Q(AuthorSymbol=result) |
            Q(Heading__startswith=keyword)
        ).distinct("Heading").order_by("Heading")

        for item in items:
            title = str(item.AuthorSymbol_id) + " | " + str(item.Heading)
            if '新規作成' in str(item.Heading):
                title += " " + str(result.AuthorName)
            preview = {
                "title": title,
                "url": reverse('author_code:Author', kwargs={'pk': item.pk}),
            }
            symbol_list.append(preview)

    data = {
        'symbol_list': symbol_list,
    }

    return JsonResponse(data)


def ajax_usedsymbol_search(request):
    keyword = {
        "LanguageCode": request.GET.get("LanguageCode"),
        "SubjectCode": request.GET.get("SubjectCode"),
        "AuthorSymbol": request.GET.get("AuthorSymbol"),
    }
    symbol_list = []

    if keyword:
        results = AuthorSymbol.objects.filter(
            LanguageCode=keyword["LanguageCode"],
            SubjectCode=keyword["SubjectCode"],
            AuthorSymbol__icontains=keyword["AuthorSymbol"],
        ).order_by("AuthorSymbol")

        if len(results) != 0:
            for result in results:
                preview = str(result.AuthorSymbol) + " | " + result.AuthorId.Heading
                symbol_list.append(preview)

        else:
            symbol_list.append("指定の言語記号、分類記号で使用されている著者記号はありません")

    data = {
        'symbol_list': symbol_list,
    }

    return JsonResponse(data)


def ajax_maintenance_author_symbol(request):
    id = request.POST.get('id')
    if id:
        task = merge.delay(id)
        data = {
            'task_id': task.id
        }
        return JsonResponse(data)
    return None


def ajax_maintenance_work_number(request):
    task = recalculation.delay()
    max_count = Work.objects.all().count()
    data = {
        'task_id': task.id,
        'max_count': max_count
    }
    return JsonResponse(data)


def ajax_bulk_create_works(request):
    extension = request.FILES['data'].name.split(".")[1].lower()
    if extension == ".csv":
        df = pd.read_csv(request.FILES['data'], header=None, dtype=str, na_filter=False)
    else:
        df = pd.read_table(request.FILES['data'], header=None, dtype=str, na_filter=False)

    if not df.empty:
        task = bulk_create_works.delay(df.to_json())
        data = {
            'task_id': task.id,
        }
        return JsonResponse(data)
    return None
