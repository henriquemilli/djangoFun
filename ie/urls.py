from django.urls import path
from django.urls.conf import include
from .views import ImportView, CustomerView



app_name = 'ie'

urlpatterns = [
    path('upload', ImportView.as_view(), name='upload'),
    path('upload/remote', ImportView.remoteImport, name='remoteimport'),
    path('view', CustomerView.as_view(), name='view'),
]