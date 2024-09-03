from django.contrib import admin
from .models import CutterSanbornThreeFigureAuthorTable, LanguageCode, SubjectCode, Author, AuthorSymbol, Work


class AuthorAdmin(admin.ModelAdmin):
    ordering = ('AuthorSymbol',)
    search_fields = ('Heading',)


class AuthorSymbolAdmin(admin.ModelAdmin):
    ordering = ('LanguageCode', 'SubjectCode', 'AuthorSymbol')
    search_fields = ('LanguageCode', 'SubjectCode', 'AuthorSymbol',)

# Register your models here.


admin.site.register(CutterSanbornThreeFigureAuthorTable)
admin.site.register(LanguageCode)
admin.site.register(SubjectCode)
admin.site.register(Author, AuthorAdmin)
admin.site.register(AuthorSymbol, AuthorSymbolAdmin)
admin.site.register(Work)