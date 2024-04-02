from django.urls import path, include

from portfolio import views

urlpatterns = [
    path('portfolio/', views.PortfolioView.as_view()),
    path('buy_stock/', views.BuyStockView.as_view()),
    path('buy_crypto/', views.BuyCryptoView.as_view()),
]