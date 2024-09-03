from django.db import models
import uuid


# Create your models here.


class CutterSanbornThreeFigureAuthorTable(models.Model):
    AuthorSymbol = models.CharField(verbose_name='Author Symbol', help_text='カッター・サンボーン著者記号', max_length=4, unique=True,
                                    primary_key=True,
                                    null=False,
                                    blank=True)
    AuthorName = models.CharField(verbose_name='Author Name', help_text='著者名', max_length=50, null=False, blank=False)

    def __str__(self):
        return str(self.AuthorSymbol)


class LanguageCode(models.Model):
    LanguageCode = models.CharField(verbose_name='Language Code', help_text='言語記号', max_length=3, unique=True,
                                    primary_key=True,
                                    null=False, blank=False)
    Language = models.CharField(verbose_name='Language', help_text='言語名', max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.LanguageCode) + " | " + str(self.Language)


class SubjectCode(models.Model):
    SubjectCode = models.CharField(verbose_name='Subject Code', help_text='主題', max_length=6, unique=True,
                                   primary_key=True,
                                   null=False, blank=False)
    Language = models.CharField(verbose_name='Language', help_text='言語名', max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.SubjectCode) + " | " + str(self.Language)


class Author(models.Model):
    AuthorId = models.UUIDField(verbose_name='Author ID', primary_key=True, unique=True, editable=False,
                                default=uuid.uuid4)
    AuthorSymbol = models.ForeignKey(CutterSanbornThreeFigureAuthorTable, verbose_name='Author Symbol',
                                     help_text='カッター・サンボーン著者記号', related_name='Author', on_delete=models.CASCADE)
    Heading = models.CharField(verbose_name='Heading', help_text='著者名', max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.AuthorSymbol) + " | " + str(self.Heading)

    class Meta:
        unique_together = ('AuthorSymbol', 'Heading')


class AuthorSymbol(models.Model):
    AuthorSymbolId = models.UUIDField(verbose_name='Author Symbol ID', primary_key=True, unique=True, editable=False,
                                      default=uuid.uuid4)
    AuthorId = models.ForeignKey(Author, verbose_name='Author ID', help_text='著者名', related_name='Symbol',
                                 on_delete=models.CASCADE)
    LanguageCode = models.ForeignKey(LanguageCode, verbose_name='Language Code', help_text='言語記号',
                                     related_name='Authors', on_delete=models.CASCADE)
    SubjectCode = models.ForeignKey(SubjectCode, verbose_name='Subject Code', help_text='請求記号２段目',
                                    on_delete=models.CASCADE)
    AuthorSymbol = models.CharField(verbose_name='Author Symbol', help_text='著者記号', max_length=50, null=False,
                                    blank=False)

    def __str__(self):
        return str(self.LanguageCode.LanguageCode) + "/" + str(self.SubjectCode.SubjectCode) + "/" + str(self.AuthorSymbol)

    class Meta:
        unique_together = ('AuthorId', 'LanguageCode', 'SubjectCode', 'AuthorSymbol')


class Work(models.Model):
    WorkId = models.UUIDField(verbose_name='Work ID', primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    AuthorSymbolId = models.ForeignKey(AuthorSymbol, verbose_name='Author Symbol ID', help_text='著者記号',
                                       related_name='Work', on_delete=models.CASCADE)
    WorkNumber = models.CharField(verbose_name='Work Number', help_text='作品番号', max_length=20, default="0", null=False,
                                  blank=False)
    WN = models.IntegerField(verbose_name='WN', help_text='ソート用WorkNumber', null=True, blank=True)
    SeriesNumber = models.CharField(verbose_name='Series Number', help_text='シリーズ番号', max_length=20, null=True,
                                    blank=True)
    SN = models.IntegerField(verbose_name='SN', help_text='ソート用SeriesNumber', null=True, blank=True)
    BookTitle = models.CharField(verbose_name='Book Title', help_text='書名', max_length=250, null=False, blank=False)
    BookId = models.CharField(verbose_name='Book ID', help_text='図書ID', max_length=10, null=False, blank=False)

    def __str__(self):
        if len(str(self.SeriesNumber)) == 0:
            if self.WorkNumber == '0':
                return str(self.AuthorSymbolId)
            else:
                return str(self.AuthorSymbolId) + '-' + str(self.WorkNumber)
        else:
            return str(self.AuthorSymbolId) + '-' + str(self.WorkNumber) + "/" + str(self.SeriesNumber)

    class Meta:
        unique_together = ('AuthorSymbolId', 'WorkNumber', 'SeriesNumber')
