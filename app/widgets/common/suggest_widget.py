from django import forms


class SuggestWidget(forms.Select):
    template_name = 'pub_stock/widgets/suggest.html'

    class Media:
        js = ['pub_stock/js/widgets/widget_suggest.js']
        css = {
            'all': ['pub_stock/css/widgets/suggest.css']
        }

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' suggest'
        else:
            self.attrs['class'] = 'suggest'