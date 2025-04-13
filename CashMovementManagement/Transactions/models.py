from datetime import date

from django.db import models

"""
Models:
    Transaction
        - date - The date of creation of the record is filled out automatically, but can be changed manually.
        - status - Status of the transaction. Foreign key.
        - type - Type of the transaction. Foreign key.
        - category - Contains category of transaction. Foreign key.
        - subcategory - Contains subcategory of transaction. Foreign key. 
            Note: Subcategory is regular category with not null parent_category
        - amount - Amount of funds in rubles. Specified with an accuracy of two decimal places.
        - description - free-form commentary to the entry (optional).
    
    Status
        - name - Name of the status. Example: "Бизнес" "Личное" "Налог"
    
    Type
        - name - Name of the type. Example: "Пополнение" "Списание"
    
    Category
        - name - Name of the category. Example: "VPS" "Avito"
        - parent_category - Parent category (optional). Example: "Инфраструктура" "Маркетинг"
        
"""
class Transaction(models.Model):
    date = models.DateField(default=date.today)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='transactions')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='transactions_of_category')
    subcategory = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='transactions_of_subcategory')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.date} - {self.status} - {self.type} - {self.category} - {self.amount} - {self.description}'

    class Meta:
        # verbose_name = 'Транзакция'
        # verbose_name_plural = 'Транзакции'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['date']


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        # verbose_name = 'Статус'
        # verbose_name_plural = 'Статусы'
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
        ordering = ['name']


class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        # verbose_name = 'Тип'
        # verbose_name_plural = 'Типы'
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True,
    )
    type = models.ForeignKey('Type', on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        if self.parent_category is None:
            return f'{self.name}'
        return f'{self.name}'

    class Meta:
        # verbose_name = 'Категория'
        # verbose_name_plural = 'Категории'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ('name', 'parent_category', 'type')

