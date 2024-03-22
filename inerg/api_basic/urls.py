# urls.py
from django.urls import path
from .views import AnnualDataView

urlpatterns = [
    path('data/', AnnualDataView.as_view(), name='annual-data'),
]
