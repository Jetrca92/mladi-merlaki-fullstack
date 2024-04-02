from django.urls import path, include

from marketdata import views


urlpatterns = [
    path('stocks/', views.StockmarketDataView.as_view()),
    path('stocks/<int:id>/', views.StockDataView.as_view()),
    path('crypto/', views.CryptomarketDataView.as_view()),
]