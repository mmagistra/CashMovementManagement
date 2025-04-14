from django.contrib import admin
from django_filters import FilterSet, DateFilter

from Transactions.models import Transaction


# Can filter categories by type
class CategoryFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'category'
    def lookups(self, request, model_admin):
        if 'type__id__exact' in request.GET:
            id = request.GET['type__id__exact']
            categories = set([c.category for c in model_admin.model.objects.all().filter(type=id)])
        else:
            categories = set([c.category for c in model_admin.model.objects.all()])
        return [(t.id, t.name) for t in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())


# Can filter subcategories by category and type
class SubcategoryFilter(admin.SimpleListFilter):
    title = 'subcategory'
    parameter_name = 'subcategory'
    def lookups(self, request, model_admin):
        if 'category' in request.GET:
            id = request.GET['category']
            subcategories = set([c.subcategory for c in model_admin.model.objects.all().filter(category=id)])
        elif 'type__id__exact' in request.GET:
            id = request.GET['type__id__exact']
            subcategories = set([c.subcategory for c in model_admin.model.objects.all().filter(type=id)])
        else:
            subcategories = set([c.subcategory for c in model_admin.model.objects.all()])
        return [(t.id, t.name) for t in subcategories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory__id__exact=self.value())


# Can filter transactions by date, status, type, category and subcategory
class TransactionFilter(FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr="gte")
    end_date = DateFilter(field_name='date', lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date', 'status', 'type', 'category', 'subcategory']
