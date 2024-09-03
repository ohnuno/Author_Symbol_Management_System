from urllib.parse import urlencode
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View, DetailView, CreateView
from author_code.models import CutterSanbornThreeFigureAuthorTable, Author, AuthorSymbol
from author_code.forms import AuthorForm


class AuthorRequest(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト"""
        try:
            author = Author.objects.get(AuthorId=kwargs["pk"])

            if author.Heading == "(新規作成)":
                url = reverse('author_code:AuthorCreate')
                param = urlencode({
                    'symbol': author.AuthorSymbol_id,
                })
                url = f'{url}?{param}'
                return redirect(url)

            else:
                return redirect('author_code:AuthorDetail', pk=author.AuthorId)

        except Author.DoesNotExist:
            raise Http404("No Author matches the given query")


class AuthorDetail(DetailView):
    template_name = "author_code/detail_Author.html"
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        try:
            symbol_list = AuthorSymbol.objects.filter(AuthorId=pk).order_by('LanguageCode')
            context["symbol_list"] = symbol_list
        except AuthorSymbol.DoesNotExist:
            pass

        return context


class AuthorCreate(CreateView):
    template_name = "author_code/create_Author.html"
    model = Author
    form_class = AuthorForm

    def get_initial(self):
        initial = super().get_initial()
        symbol = CutterSanbornThreeFigureAuthorTable.objects.get(AuthorSymbol=self.request.GET['symbol'])
        initial['AuthorSymbol'] = symbol
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbol = self.request.GET['symbol']
        context['author'] = {
            'AuthorSymbol_id': symbol,
            'Heading': '(新規作成)',
        }
        return context

    def get_success_url(self):
        return reverse('author_code:AuthorDetail', kwargs={'pk': self.object.AuthorId})