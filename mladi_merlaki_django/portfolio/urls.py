from django.urls import path, include

from portfolio import views

urlpatterns = [
    path('portfolio/', views.PortfolioView.as_view()),
]