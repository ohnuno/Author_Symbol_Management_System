from django import forms
from .models import Author, AuthorSymbol, Work


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('AuthorSymbol', 'Heading')
        widgets = {
            'Heading': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['AuthorSymbol'].widget = forms.HiddenInput()


class AuthorSymbolForm(forms.ModelForm):

    class Meta:
        model = AuthorSymbol
        fields = ('AuthorId', 'LanguageCode', 'SubjectCode', 'AuthorSymbol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['AuthorId'].widget = forms.HiddenInput()
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control ajax-search-usedsymbol"


class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ('AuthorSymbolId', 'WorkNumber', 'WN', 'SeriesNumber', 'SN', 'BookTitle', 'BookId')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['AuthorSymbolId'].widget = forms.HiddenInput()
        self.fields['WN'].widget = forms.HiddenInput()
        self.fields['SN'].widget = forms.HiddenInput()
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
