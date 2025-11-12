# urls.py
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from text2sql import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/generate_sql/', views.generate_sql, name='generate_sql_api'),
]
