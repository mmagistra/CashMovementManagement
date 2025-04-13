from dal import autocomplete
from django.shortcuts import render
from django.views.generic import FormView

from Transactions.forms import CategoryForm
from Transactions.models import Category


class ParentCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.all()
        qs = qs.filter(parent_category__isnull=True)

        type = self.forwarded.get('type', None)

        if type:
            qs = qs.filter(type=type)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.all()
        qs = qs.filter(parent_category__isnull=True)

        type = self.forwarded.get('type', None)

        if type:
            qs = qs.filter(type=type)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SubcategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.all()
        qs = qs.filter(parent_category__isnull=False)

        category = self.forwarded.get('category', None)

        if category:
            qs = qs.filter(parent_category=category)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
