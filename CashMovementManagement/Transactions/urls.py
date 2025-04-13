from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name

from .admin_views import (
    ParentCategoryAutocomplete,
    CategoryAutocomplete,
    SubcategoryAutocomplete
)
from .views import TransactionViewSet, CategoryViewSet, TypeViewSet, StatusViewSet

app_name = 'Transactions'

router = DefaultRouter()
router.register('transactions', TransactionViewSet, 'transaction')
router.register('categories', CategoryViewSet, 'category')
router.register('types', TypeViewSet, 'type')
router.register('statuses', StatusViewSet, 'status')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'autocomplete/parent_category_autocomplete',
        ParentCategoryAutocomplete.as_view(),
        name='parent-category-autocomplete'
    ),
    path(
        'autocomplete/category_autocomplete',
        CategoryAutocomplete.as_view(),
        name='category-autocomplete'
    ),
    path(
        'autocomplete/subcategory_autocomplete',
        SubcategoryAutocomplete.as_view(),
        name='subcategory-autocomplete'
    ),
]
