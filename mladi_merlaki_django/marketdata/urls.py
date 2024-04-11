from django.urls import path, include

from marketdata import views


urlpatterns = [
    path('stocks/', views.StockmarketDataView.as_view()),
    path('stocks/<int:id>/', views.StockDataView.as_view()),
    path('crypto/', views.CryptomarketDataView.as_view()),
    path('crypto/<int:id>/', views.CryptocurrencyDataView.as_view()),
    path('app_data/', views.AppdataView.as_view()),
]
