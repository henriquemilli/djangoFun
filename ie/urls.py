from django.urls import path
from django.urls.conf import include
from .views import CustomerView, FtpView, UploadView



app_name = 'ie'

urlpatterns = [
    path('upload', UploadView.as_view(), name='upload'),
    path('view', CustomerView.as_view(), name='view'),
    path('ftp', FtpView.as_view(), name='ftp'),
    path('ftp/result', FtpView.upload_from_ftp, name='ftp-result'),
]