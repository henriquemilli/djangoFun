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
            origin_list = [ form.instance.file.path ]
            self.localImport(origin_list)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def localImport(request, origin_list): 
        destination_obj = Cliente

        try:
            functions.localImport(origin_list, destination_obj)
            return redirect('win')
        except:
            return redirect('fail')

    def remoteImport(request):
        destination_obj = Cliente
        local_register = PulledCsv
        
        try:
            functions.remoteImport(destination_obj, local_register)
            return render(request, 'opwin.html')
        except:
            return render(request, 'opfail.html')
    


class CustomerView(LoginRequiredMixin, ListView):
    template_name = 'ie/view.html'
    context_object_name = 'customers'
    queryset = Cliente.objects.all()