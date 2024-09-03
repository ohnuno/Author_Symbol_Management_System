from celery.result import AsyncResult
from django.http import JsonResponse


def task_info(request, task_id):
    task = AsyncResult(task_id)
    data = {
        'state': task.state,
    }
    if task.state == 'PROGRESS':
        data['counter'] = task.info.get('counter', 0)
        data['message'] = task.info.get('message', 0)
        data['max'] = task.info.get('max', 0)
    elif task.state == 'SUCCESS':
        data['result'] = task.result
    elif task.state == 'PENDING':
        data['message'] = 'データを読込中です...'
    elif task.state == 'FAILURE':
        try:
            data['message'] = task.info.get('message', 0)
        except AttributeError as e:
            data['message'] = task.traceback

    return JsonResponse(data)
