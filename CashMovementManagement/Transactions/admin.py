from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder
from django.contrib.admin import site as admin_site

from .forms import CategoryForm, TransactionForm
from .models import Transaction, Category, Status, Type
from .filters import CategoryFilter, SubcategoryFilter


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # fields which will ve displayed
    list_display = ('pk', 'date', 'status', 'type', 'category', 'subcategory', 'amount', 'description')
    list_display_links = ('pk', )
    # fields which will be filtered. date is a DateRangeFilter which filters by range between two dates
    list_filter = (('date', DateRangeFilterBuilder()), 'status', 'type', CategoryFilter, SubcategoryFilter)
    form = TransactionForm

    class Media:
        js = ('js/admin/clear_fields.js',)

    # radio_fields = {'status': admin.HORIZONTAL}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'parent_category', 'type')
    list_display_links = ('pk', )
    list_filter = ('name', 'parent_category', 'type')
    form = CategoryForm

    class Media:
        # Connecting js file for auto clearing fields
        js = ('js/admin/clear_fields.js',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', )
    list_filter = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', )
    list_filter = ('name',)


# grouping models in admin menu
def group_models(*groups):
    def decorator(f):
        def wrapper(*args, **kwargs):
            app_list = f(*args, **kwargs)

            new_app_list = []
            for group in groups:
                models = []
                for app_label, model_name in group['models']:
                    for app in app_list:
                        for model in app['models']:
                            if model['object_name'] == model_name and app['app_label'] == app_label:
                                models.append(model)
                                break
                if models:
                    new_app_list.append({
                        'name': group['name'],
                        'models': models,
                    })

            return new_app_list

        return wrapper

    return decorator


admin_site.get_app_list = group_models(
    {
        'name': 'Users',
        'models': [('auth', 'User'), ('auth', 'Group')]
    },
    {
        'name': 'Transactions',
        'models': [('Transactions', 'Transaction')]
    },
    {
        'name': 'Reference books',
        'models': [('Transactions', 'Status'), ('Transactions', 'Type'), ('Transactions', 'Category')]
    }
)(admin_site.get_app_list)

