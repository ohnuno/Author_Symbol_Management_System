from django.views.generic import TemplateView


# Create your views here.


class Upload(TemplateView):
    template_name = 'author_code/upload_AuthorSymbol.html'
