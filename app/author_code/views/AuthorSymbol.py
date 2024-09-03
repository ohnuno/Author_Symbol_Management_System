from urllib.parse import urlencode
from django.urls import reverse
from django.views.generic import DetailView, CreateView, DeleteView
from author_code.models import Author, AuthorSymbol, Work
from author_code.forms import AuthorSymbolForm
import uuid


class AuthorSymbolDetail(DetailView):
    template_name = "author_code/detail_AuthorSymbol.html"
    model = AuthorSymbol

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        try:
            work_list = Work.objects.filter(AuthorSymbolId=pk).order_by("WN", "SN")
            context["work_list"] = work_list
        except Work.DoesNotExist:
            pass

        return context


class AuthorSymbolCreate(CreateView):
    template_name = "author_code/create_AuthorSymbol.html"
    model = AuthorSymbol
    form_class = AuthorSymbolForm

    def get_initial(self):
        initial = super().get_initial()
        author = Author.objects.get(AuthorId=self.request.GET['author'])
        initial = {
            'AuthorId': author,
            'SubjectCode': "9□-8",
            'AuthorSymbol': author.AuthorSymbol
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(AuthorId=uuid.UUID(self.request.GET['author']))
        context['author'] = author
        return context

    def get_success_url(self):
        url = "".join([reverse('author_code:WorkCreate'), '?', urlencode(dict(symbol=self.object.AuthorSymbolId))])
        return url


class AuthorSymbolDelete(DeleteView):
    template_name = "author_code/delete_AuthorSymbol.html"
    model = AuthorSymbol

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        other_symbol = AuthorSymbol.objects.filter(AuthorId=self.object.AuthorId_id).count()
        if other_symbol == 0:
            author = Author.objects.get(AuthorId=self.object.AuthorId_id)
            author.delete()
        return result

    def get_success_url(self):
        url = reverse('author_code:index')
        return url
