from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from datetime import datetime
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseListView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = Expense.objects.filter(user=user)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset

class ExpenseAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)

        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        category_wise = (
            expenses.values('category')
            .annotate(total=Sum('amount'))
        )

        

        return Response({
            'total_expenses': total,
            'category_breakdown': category_wise,
        })


# Create your views here.
