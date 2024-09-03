from django.views.generic import TemplateView
from django_pandas.io import read_frame
from django import forms
from author_code.models import AuthorSymbol


class AuthorSymbolMaintenance(TemplateView):
    template_name = 'author_code/maintenance_author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # AuthorSymbol の抽出
        df = read_frame(AuthorSymbol.objects.all(), fieldnames=[
            'AuthorSymbolId',
            'AuthorId__Heading',
            'LanguageCode__LanguageCode',
            'SubjectCode__SubjectCode',
            'AuthorSymbol',
        ]).rename(columns={
            'AuthorId__Heading': 'Heading',
            'LanguageCode__LanguageCode': 'LanguageCode',
            'SubjectCode__SubjectCode': 'SubjectCode',
        })
        # 重複の削除
        df = df[df.duplicated(
            keep=False,
            subset=[
                'LanguageCode',
                'SubjectCode',
                'AuthorSymbol',
            ]
        )]
        # LanguageCode, SubjectCode, AuthorSymbol でマルチインデックス化
        df = df.sort_values(['LanguageCode', 'SubjectCode', 'AuthorSymbol'])
        df = df.set_index(['LanguageCode', 'SubjectCode', 'AuthorSymbol'])

        # form の作成
        form_list = []
        for index, data in df.groupby(level=['LanguageCode', 'SubjectCode', 'AuthorSymbol']):
            get_tuple = lambda x: (x['AuthorSymbolId'], x['Heading'])
            data['choice'] = data.apply(get_tuple, axis=1)
            choices = data['choice'].to_list()
            form = MaintenanceForm()
            form.fields['select'].label = '/'.join(str(x) for x in index)
            form.fields['select'].choices = choices
            form_list.append(form)

        context['form_list'] = form_list
        return context

class MaintenanceForm(forms.Form):
    select = forms.ChoiceField(widget=forms.RadioSelect)