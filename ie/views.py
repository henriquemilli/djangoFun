from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.urls.base import is_valid_path
from .models import RemoteSimple, Simple
from .forms import CsvModelForm
from django.views.generic import ListView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin



class UploadView(LoginRequiredMixin, FormView):
    template_name = 'ie/upload.html'
    success_url = 'view'
    form_class = CsvModelForm

    
    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            form.save()
            filepath = form.instance.file.path
            Simple.importFromCsv(Simple, filepath)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FtpView(LoginRequiredMixin, TemplateView):
    template_name = 'ie/ftp.html'
    context_object_name = 'ftp'

    def upload_from_ftp(request):
        try:
            RemoteSimple.sync(RemoteSimple)
            return render(request, 'ie/opwin.html')
        except Exception as e:
            print(e)
            return render(request, 'ie/opfail.html')   


class CustomerView(LoginRequiredMixin, ListView):
    template_name = 'ie/view.html'
    context_object_name = 'customers'
    queryset = Simple.objects.all()
    
