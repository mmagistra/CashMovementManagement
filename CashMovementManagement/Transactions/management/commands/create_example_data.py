from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from Transactions.models import Transaction, Category, Status, Type


UserModel = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating test data')

        print('Creating admin if not exists')
        if UserModel.objects.filter(username='admin').exists():
            print('- Admin already exists')
        else:
            print('Creating admin...')
            # Create a superuser
            User.objects.create_superuser(
                username='admin',
                email='lXK7t@example.com',
                password='admin',
            )
            print('+ Admin created')

        example_data = {
            'status': [
                {'name': 'Бизнес'},
                {'name': 'Личное'},
                {'name': 'Налог'},
            ],
            'type': [
                {'name': 'Пополнение'},
                {'name': 'Списание'},
            ],
            'category': [
                {'name': 'Инфраструктура', 'parent_category': None, 'type': 'Пополнение'},
                {'name': 'Маркетинг', 'parent_category': None, 'type': 'Списание'},
            ],
            'subcategory': [
                {'name': 'VPS', 'parent_category': 'Инфраструктура', 'type': 'Пополнение'},
                {'name': 'Proxy', 'parent_category': 'Инфраструктура', 'type': 'Пополнение'},
                {'name': 'Farpost', 'parent_category': 'Маркетинг', 'type': 'Списание'},
                {'name': 'Avito', 'parent_category': 'Маркетинг', 'type': 'Списание'},
            ],
            'transaction': [
                {
                    'date': date(2025, 4, 1),
                    'status': 'Бизнес',
                    'type': 'Пополнение',
                    'category': 'Инфраструктура',
                    'subcategory': 'VPS',
                    'amount': 1000,
                    'description': 'Пополнение VPS',
                },
                {
                    'date': date(2025, 4, 3),
                    'status': 'Налог',
                    'type': 'Пополнение',
                    'category': 'Инфраструктура',
                    'subcategory': 'Proxy',
                    'amount': 200,
                    'description': 'Пополнение Proxy',
                },
                {
                    'date': date(2025, 4, 2),
                    'status': 'Личное',
                    'type': 'Списание',
                    'category': 'Маркетинг',
                    'subcategory': 'Farpost',
                    'amount': 500,
                    'description': 'Продажа Farpost',
                },
                {
                    'date': date(2025, 4, 4),
                    'status': 'Личное',
                    'type': 'Списание',
                    'category': 'Маркетинг',
                    'subcategory': 'Avito',
                    'amount': 1000,
                    'description': 'Продажа Avito',
                }
            ],
        }

        print('Creating example data...')

        for model, data in example_data.items():
            for item in data:
                if model == 'status':
                    status = Status.objects.get_or_create(**item)
                    if status[1]:
                        print(f'+ Status "{status[0]}" created')
                    else:
                        print(f'- Status "{status[0]}" already exists')
                elif model == 'type':
                    transaction_type = Type.objects.get_or_create(**item)
                    if transaction_type[1]:
                        print(f'+ Type "{transaction_type[0]}" created')
                    else:
                        print(f'- Type "{transaction_type[0]}" already exists')
                elif model == 'category':
                    item['type'] = Type.objects.get(name=item['type'])
                    category = Category.objects.get_or_create(**item)
                    if category[1]:
                        print(f'+ Category "{category[0]}" created')
                    else:
                        print(f'- Category "{category[0]}" already exists')
                elif model == 'subcategory':
                    item['type'] = Type.objects.get(name=item['type'])
                    item['parent_category'] = Category.objects.get(name=item['parent_category'])
                    subcategory = Category.objects.get_or_create(**item)
                    if subcategory[1]:
                        print(f'+ Subcategory "{subcategory[0]}" created')
                    else:
                        print(f'- Subcategory "{subcategory[0]}" already exists')
                elif model == 'transaction':
                    item['status'] = Status.objects.get(name=item['status'])
                    item['type'] = Type.objects.get(name=item['type'])
                    item['category'] = Category.objects.get(name=item['category'])
                    item['subcategory'] = Category.objects.get(name=item['subcategory'])
                    transaction = Transaction.objects.get_or_create(**item)
                    if transaction[1]:
                        print(f'+ Transaction "{transaction[0]}" created')
                    else:
                        print(f'- Transaction "{transaction[0]}" already exists')

        print('Test data created')
