from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.views.generic import ListView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Csv, PulledCsv, Cliente
from .forms import CsvModelForm
from . import functions



class ImportView(LoginRequiredMixin, FormView):
    template_name = 'ie/upload.html'
    success_url = 'win'
    form_class = CsvModelForm


    def post(self, request, *args, **kwargs):

        form = self.get_form()

        if form.is_valid():
            form.save()
            origin_list = [form.instance.file.path]
            self.localImport(origin_list)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def localImport(request, origin_list):
        functions.localImport(origin_list)


    def remoteImport(request):
        try:
            functions.remoteImport()
            return render(request, 'opwin.html')
        except:
            return render(request, 'opfail.html')
    


class CustomerView(LoginRequiredMixin, ListView):
    template_name = 'ie/view.html'
    context_object_name = 'customers'
    queryset = Cliente.objects.all()