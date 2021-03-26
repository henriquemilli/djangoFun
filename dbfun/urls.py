from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from .views import HomeView, WinView, FailView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('win', WinView.as_view(), name='win'),
    path('fail', WinView.as_view(), name='fail'), 
    path('', HomeView.as_view(), name='home'),
    path('', include('ie.urls', namespace='ie')),
    path('', include('users.urls', namespace='users')),
    path('mail/', include('mail.urls', namespace='mail')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)