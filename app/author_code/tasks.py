from __future__ import absolute_import, unicode_literals

import traceback

import pandas as pd
from celery import shared_task, states
from celery.exceptions import Ignore
from author_code.models import AuthorSymbol, Work
from widgets.author_code.calc_series_no import calc_work_no, calc_series_no
from widgets.author_code.bulk_create import Data, NotProperCSVError
from django_pandas.io import read_frame


@shared_task(bind=True)
def merge(self, id):
    try:
        symbol_after = AuthorSymbol.objects.get(pk=id)
        symbol_before = AuthorSymbol.objects.filter(
            LanguageCode=symbol_after.LanguageCode,
            SubjectCode=symbol_after.SubjectCode,
            AuthorSymbol=symbol_after.AuthorSymbol
        ).exclude(pk=id)
        if symbol_before.exists():
            for symbol in symbol_before:
                works = Work.objects.filter(AuthorSymbolId=symbol)
                bulk_list = []
                for work in works:
                    work.AuthorSymbolId = symbol_after
                    bulk_list.append(work)
                Work.objects.bulk_update(bulk_list, fields=['AuthorSymbolId'])
                if AuthorSymbol.objects.filter(AuthorId=symbol.AuthorId).count() == 1:
                    symbol.AuthorId.delete()

    except Exception as e:
        self.update_state(
            state=states.FAILURE,
            meta=e
        )
        raise Ignore()


@shared_task(bind=True)
def recalculation(self):
    try:
        df = read_frame(Work.objects.all(), fieldnames=[
            'WorkId', 'WorkNumber', 'SeriesNumber'
        ])
        df['WN'] = df['WorkNumber'].apply(calc_work_no)
        df['SN'] = df['SeriesNumber'].apply(calc_series_no)
        bulk_work = df.apply(get_bulk_work_4_update, task=self, axis=1).to_list()
        Work.objects.bulk_update(bulk_work, batch_size=5000, fields=['WN', 'SN'])

    except Exception as e:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(e).__name__,
                'exc_message': traceback.format_exc().split('\n'),
                'message': e
            }
        )
        raise Ignore()


def get_bulk_work_4_update(series, task):
    item = Work(
        WorkId=series['WorkId'],
        WN=series['WN'],
        SN=series['SN'],
    )
    task.update_state(
        state='PROGRESS',
        meta={'counter': series.name + 1},
    )
    return item


@shared_task(bind=True)
def bulk_create_works(self, json):
    try:
        data = Data(pd.read_json(json))
    except ValueError as e:
        message = '読み込んだファイルのフィールド数が適切ではありません。\nデータに区切記号が含まれていないか確認してください。\n\n' + str(e)
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(e).__name__,
                'exc_message': traceback.format_exc().split('\n'),
                'message': message
            }
        )
        raise Ignore()

    try:
        self.update_state(
            state='PROGRESS',
            meta={'message': 'カッターサンボーン著者記号を処理中...'},
        )
        data.set_cutter()
        self.update_state(
            state='PROGRESS',
            meta={'message': '著者を処理中...'},
        )
        data.set_author()
        self.update_state(
            state='PROGRESS',
            meta={'message': '言語記号を処理中...'},
        )
        data.set_language()
        self.update_state(
            state='PROGRESS',
            meta={'message': '請求記号２段目を処理中...'},
        )
        data.set_subject()
        self.update_state(
            state='PROGRESS',
            meta={'message': '著者記号を処理中...'},
        )
        data.set_author_symbol()
        self.update_state(
            state='PROGRESS',
            meta={'message': '作品番号・シリーズ番号を処理中...'},
        )
        data.set_serial_no()
        self.update_state(
            state='PROGRESS',
            meta={'message': '著作を登録中...'},
        )
        data.set_work()
        return str(len(data.df)) + '件のデータを登録しました。'

    except NotProperCSVError as e:
        self.update_state(
            state=states.FAILURE,
            meta={'message': e}
        )
        raise Ignore()
