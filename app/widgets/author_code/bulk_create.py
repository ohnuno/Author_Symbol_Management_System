import re
import pandas as pd
from author_code.models import CutterSanbornThreeFigureAuthorTable, Author, LanguageCode, SubjectCode, AuthorSymbol, \
    Work
from widgets.author_code.calc_series_no import calc_series_no


class Data:
    """
    CSVデータの検証, データ一括作成用クラス
    """

    def __init__(self, df):
        self.df = df
        self.df.set_axis([
            'cutter', 'author', 'language', 'subject', 'author_symbol', 'work_no', 'ser_no', 'title', 'id'
        ], axis='columns', inplace=True
        )
        # author_symbolの同定用に'言語記号/主題/著者記号'の文字列を保持しておく
        self.df['author_symbol_str'] = self.df['language'] + '/' + self.df['subject'] + '/' + self.df['author_symbol']

    def set_cutter(self):
        """
        カッター・サンボーンモデルの取得
        """
        # CSV の 'cutter' フィールドを重複削除し、該当するモデルを抽出
        cutter_list = self.df['cutter'].drop_duplicates().tolist()
        cutters = CutterSanbornThreeFigureAuthorTable.objects.filter(AuthorSymbol__in=cutter_list)
        # 抽出したクエリセットから辞書を作成し、dataframeに含まれるカッター・サンボーンをモデルと置換
        cutters = {
            cutter.AuthorSymbol: cutter for cutter in cutters
        }
        self.df['cutter'] = self.df['cutter'].map(cutters)

        # 登録済みのカッター・サンボーンと合致しないものが入力されている場合にはエラーを返す
        if self.df['cutter'].isnull().any():
            errors = self.df[self.df['cutter'].isnull()].index.values.tolist()
            message = '以下の行で指定されているカッターサンボーン著者記号は適正な値ではありません。\n'
            for index in errors:
                message += str(int(index) + 1) + '行目\n'
            raise NotProperCSVError(message)

    def set_author(self):
        """
        著者の新規一括作成と self.df へのモデルセット
        """
        # CSV の 'author' フィールドを対象に重複削除
        author_list = self.df.drop_duplicates(subset='author')
        # Author モデルの bulk_create
        create_author = lambda row: Author(AuthorSymbol=row['cutter'], Heading=row['author'])
        author_bulk = author_list.apply(create_author, axis=1)
        author_bulk = author_bulk.to_list()
        Author.objects.bulk_create(author_bulk, ignore_conflicts=True, batch_size=5000)
        # モデルを抽出し、クエリセットから作成した辞書で 'author' フィールドをモデルと置換
        author_list = Author.objects.filter(
            Heading__in=self.df['author'].drop_duplicates().tolist()
        )
        author_list = {author.Heading: author for author in author_list}
        self.df['author'] = self.df['author'].map(author_list)

    def set_language(self):
        """
        言語記号のモデルセット
        """
        language_list = self.df['language'].drop_duplicates().tolist()
        languages = LanguageCode.objects.filter(LanguageCode__in=language_list)
        languages = {language.LanguageCode: language for language in languages}
        self.df['language'] = self.df['language'].map(languages)
        if self.df['language'].isnull().any():
            errors = self.df[self.df['cutter'].isnull()].index.values.tolist()
            message = '以下の行で指定されている言語記号は適正な値ではありません。\n'
            for index in errors:
                message += str(int(index) + 1) + '行目\n'
            raise NotProperCSVError(message)

    def set_subject(self):
        """
        主題分類 (請求記号２段目) のモデルセット
        """
        subject_list = self.df['subject'].drop_duplicates().tolist()
        subjects = SubjectCode.objects.filter(SubjectCode__in=subject_list)
        subjects = {subject.SubjectCode: subject for subject in subjects}
        self.df['subject'] = self.df['subject'].map(subjects)
        if self.df['subject'].isnull().any():
            errors = self.df[self.df['cutter'].isnull()].index.values.tolist()
            message = '以下の行で指定されている請求記号２段目は適正な値ではありません。\n'
            for index in errors:
                message += str(int(index) + 1) + '行目\n'
            raise NotProperCSVError(message)

    def set_author_symbol(self):
        """
        東外大著者記号の一括登録とモデルセット
        """
        author_symbol_list = self.df.drop_duplicates(subset=['author', 'language', 'subject', 'author_symbol'])
        create_author_symbol = lambda row: AuthorSymbol(
            AuthorId=row['author'],
            LanguageCode=row['language'],
            SubjectCode=row['subject'],
            AuthorSymbol=row['author_symbol']
        )
        author_symbol_bulk = author_symbol_list.apply(create_author_symbol, axis=1)
        author_symbol_bulk = author_symbol_bulk.to_list()
        AuthorSymbol.objects.bulk_create(author_symbol_bulk, ignore_conflicts=True, batch_size=5000)

        author_symbol_list = AuthorSymbol.objects.filter(
            AuthorId__in=self.df['author'].drop_duplicates().tolist(),
            LanguageCode__in=self.df['language'].drop_duplicates().tolist(),
            SubjectCode__in=self.df['subject'].drop_duplicates().tolist(),
            AuthorSymbol__in=self.df['author_symbol'].drop_duplicates().tolist(),
        )
        author_symbol_dict = {
            str(author_symbol): author_symbol for author_symbol in author_symbol_list
        }
        # __init__で作成した同定用文字列をベースに置換する
        self.df['author_symbol'] = self.df['author_symbol_str'].map(author_symbol_dict)

    def set_serial_no(self):
        self.df['wn'] = self.df.apply(self.get_wn, axis=1)
        self.df['sn'] = self.df['ser_no'].apply(calc_series_no)

    def set_work(self):
        self.df.replace('nan', None)
        create_work = lambda x: Work(
            AuthorSymbolId=x['author_symbol'],
            WorkNumber=x['work_no'] or 0,
            WN=x['wn'] or None,
            SeriesNumber=x['ser_no'],
            SN=x['sn'] or None,
            BookTitle=x['title'],
            BookId=str(x['id']).zfill(10)
        )
        work_bulk = self.df.apply(create_work, axis=1).tolist()
        Work.objects.bulk_create(work_bulk, ignore_conflicts=True, batch_size=5000)

    def get_wn(self, row):
        compiler = re.compile('[0-9]+')
        no = row['work_no']
        if not no:
            wn = 0
        elif compiler.findall(no):
            wn = compiler.findall(no)
            wn = int(wn[0])
        else:
            message = '以下の行で指定されている作品番号は適正な値ではありません。\n'
            message += str(int(row.index) + 1) + '行目\n'
            raise NotProperCSVError(message)

        return wn


class NotProperCSVError(Exception):
    """
    カッターサンボーンの形式が不正な場合のエラークラス
    """
    pass