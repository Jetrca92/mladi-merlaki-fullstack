from django.urls import path, include

from portfolio import views

urlpatterns = [
    path('portfolio/', views.PortfolioView.as_view()),
    path('buy_stock/', views.BuyStockView.as_view()),
    path('buy_crypto/', views.BuyCryptoView.as_view()),
    path('transactions/', views.TransactionsView.as_view()),
    path('rankings/', views.RankingsView.as_view()),
]