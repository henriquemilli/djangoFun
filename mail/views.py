from django.shortcuts import render
from django.views.generic import TemplateView


class SendView(TemplateView):
    template_name= 'mail/send.html'