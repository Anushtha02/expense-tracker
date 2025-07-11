from django.urls import path
from .views import ExpenseCreateView, ExpenseListView, ExpenseAnalyticsView

urlpatterns = [
    path('expenses/', ExpenseCreateView.as_view(), name='create-expense'),
    path('expenses/list/', ExpenseListView.as_view(), name='list-expenses'),
    path('expenses/analytics/', ExpenseAnalyticsView.as_view(), name='expense-analytics'),
]