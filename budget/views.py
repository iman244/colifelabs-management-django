from django.shortcuts import render
from rest_framework import viewsets
from .models import FinancialStatement
from .serializers import FinancialStatementSerializer

# Create your views here.
class FinancialStatementViews(viewsets.ModelViewSet):
    queryset = FinancialStatement.objects.all()
    serializer_class = FinancialStatementSerializer
    lookup_field = 'slug'