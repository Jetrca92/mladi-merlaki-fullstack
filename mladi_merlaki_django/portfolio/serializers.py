from django.contrib.auth.models import User

from rest_framework import serializers

from portfolio.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = (
            "owner",
            "cash",
            "stocks",
            "crypto",
        )