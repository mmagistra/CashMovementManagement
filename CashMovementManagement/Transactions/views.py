from rest_framework import viewsets

from .filters import TransactionFilter
from .models import Transaction, Status, Type, Category
from .serializers import TransactionSerializer, StatusSerializer, TypeSerializer, CategorySerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # use our custom filter
    filterset_class = TransactionFilter


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Can filter by type and parent category in any request
    filterset_fields = ['type', 'parent_category']
