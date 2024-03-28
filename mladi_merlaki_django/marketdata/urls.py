from django.urls import path, include

from marketdata import views


urlpatterns = [
    path('stocks/', views.StockmarketDataView.as_view()),
]