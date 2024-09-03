from django.urls import path
from .views import index
from .views import Author
from .views import AuthorSymbol
from .views import Work
from .views import upload_AuthorSymbol
from .views import upload_CutterSanbornThreeFigureAuthorTable
from .views import upload_LanguageCode
from .views import upload_Author
from .views import upload_SubjectCode
from .views import ajax
from .views import maintenance_author_symbol
from .views import maintenance_work_number

app_name = 'author_code'
urlpatterns = [
    path('', index.index.as_view(), name='index'),
    path('Author/<uuid:pk>/', Author.AuthorRequest.as_view(), name='Author'),
    path('Author/detail/<uuid:pk>/', Author.AuthorDetail.as_view(), name='AuthorDetail'),
    path('Author/create/', Author.AuthorCreate.as_view(), name='AuthorCreate'),
    path('AuthorSymbol/detail/<uuid:pk>/', AuthorSymbol.AuthorSymbolDetail.as_view(), name='AuthorSymbolDetail'),
    path('AuthorSymbol/create/', AuthorSymbol.AuthorSymbolCreate.as_view(), name='AuthorSymbolCreate'),
    path('AuthorSymbol/delete/<uuid:pk>/', AuthorSymbol.AuthorSymbolDelete.as_view(), name='AuthorSymbolDelete'),
    path('Work/edit/<uuid:pk>/', Work.WorkEdit.as_view(), name='WorkEdit'),
    path('Work/create/', Work.WorkCreate.as_view(), name='WorkCreate'),
    path('Work/delete/<uuid:pk>/', Work.WorkDelete.as_view(), name='WorkDelete'),
    path(
        'upload/CutterSanbornThreeFigureAuthorTable/',
        upload_CutterSanbornThreeFigureAuthorTable.upload, name='Upload'
    ),
    path('upload/LanguageCode/', upload_LanguageCode.upload, name='UploadLanguageCode'),
    path('upload/Author/', upload_Author.upload, name='UploadAuthor'),
    path('upload/AuthorSymbol', upload_AuthorSymbol.Upload.as_view(), name='UploadAuthorSymbol'),
    path('upload/SubjectCode/', upload_SubjectCode.upload, name='UploadSubjectCode'),
    path('ajax/authorsymbol/search/', ajax.ajax_authorsymbol_search, name='ajax_authorsymbol_search'),
    path('ajax/usedsymbol/search/', ajax.ajax_usedsymbol_search, name='ajax_usedsymbol_search'),
    path('ajax/maintenance/AuthorSymbol', ajax.ajax_maintenance_author_symbol, name='ajax_maintenance_author_symbol'),
    path('ajax/maintenance/WorkNumber', ajax.ajax_maintenance_work_number, name='ajax_maintenance_work_number'),
    path('ajax/bulk/create/works', ajax.ajax_bulk_create_works, name='ajax_bulk_create_works'),
    path('maintenance/author/', maintenance_author_symbol.AuthorSymbolMaintenance.as_view(), name='maintenance_author'),
    path('maintenance/work/', maintenance_work_number.WorkNumberMaintenance.as_view(), name='maintenance_work'),
]
