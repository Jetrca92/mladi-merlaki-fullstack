from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from portfolio.models import Portfolio
from portfolio.serializers import PortfolioSerializer


class PortfolioView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None):
        portfolio, _created = Portfolio.objects.get_or_create(owner=request.user)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)


