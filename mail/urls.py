from django.urls import path
from .views import SendView



app_name = 'mail'

urlpatterns = [
    path('send', SendView.as_view(), name='send'),
]
