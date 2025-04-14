from dal import autocomplete
from django import forms
from django.contrib import admin

from Transactions.models import Category, Transaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'parent_category']
        # widget used for autocomplete of fields
        widgets = {
            'parent_category': autocomplete.ModelSelect2(url='Transactions:parent-category-autocomplete',
                                                       forward=['type'])
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'description']

        # widget used for autocomplete of fields
        widgets = {
            'category': autocomplete.ModelSelect2(url='Transactions:category-autocomplete', forward=['type']),
            'subcategory': autocomplete.ModelSelect2(url='Transactions:subcategory-autocomplete', forward=['category']),
        }


