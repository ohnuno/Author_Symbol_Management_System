from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView
from author_code.models import AuthorSymbol, Work
from author_code.forms import WorkForm
from widgets.author_code.calc_series_no import calc_series_no, calc_work_no
import uuid


class WorkEdit(UpdateView):
    template_name = "author_code/edit_Work.html"
    model = Work
    form_class = WorkForm

    def form_valid(self, form):
        form.instance.WN = calc_work_no(form.cleaned_data["WorkNumber"])

        if form.cleaned_data["SeriesNumber"]:
            series = calc_series_no(form.cleaned_data["SeriesNumber"])
            form.instance.SN = series

        return super(WorkEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse('author_code:AuthorSymbolDetail', kwargs={'pk': self.object.AuthorSymbolId_id})


class WorkCreate(CreateView):
    template_name = "author_code/create_Work.html"
    model = Work
    form_class = WorkForm

    def get_initial(self):
        initial = super().get_initial()
        symbol = AuthorSymbol.objects.get(AuthorSymbolId=uuid.UUID(self.request.GET['symbol']))
        initial['AuthorSymbolId'] = symbol
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        symbol = AuthorSymbol.objects.get(AuthorSymbolId=uuid.UUID(self.request.GET['symbol']))
        context['symbol'] = symbol
        return context

    def form_valid(self, form):
        form.instance.WN = calc_work_no(form.cleaned_data["WorkNumber"])

        if form.cleaned_data["SeriesNumber"]:
            series = calc_series_no(form.cleaned_data["SeriesNumber"])
            form.instance.SN = series

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('author_code:AuthorSymbolDetail', kwargs={'pk': self.object.AuthorSymbolId_id})


class WorkDelete(DeleteView):
    template_name = "author_code/delete_Work.html"
    model = Work

    def get_success_url(self):
        return reverse('author_code:AuthorSymbolDetail', kwargs={'pk': self.object.AuthorSymbolId_id})
