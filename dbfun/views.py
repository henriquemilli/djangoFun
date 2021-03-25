from django.views.generic import TemplateView




class HomeView(TemplateView):
    template_name = 'home.html'



class WinView(TemplateView):
    template_name = 'opwin.html'



class FailView(TemplateView):
    template_name = 'opfail.html'