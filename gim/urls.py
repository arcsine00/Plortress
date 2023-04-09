from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gim'

urlpatterns = [
    path('', views.request, name='request'),
    path('<int:req_id>/', views.detail, name='detail'),
    path('write/', views.req_write, name='req_write'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
