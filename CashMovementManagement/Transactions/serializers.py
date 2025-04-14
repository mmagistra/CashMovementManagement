from django.contrib.admin.utils import lookup_field
from rest_framework.exceptions import ValidationError
from rest_framework.relations import HyperlinkedRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, RelatedField

from .models import Transaction, Status, Type, Category


class TransactionSerializer(ModelSerializer):
    # PrimaryKeyRelatedField is used to get the primary key of the related object
    status = PrimaryKeyRelatedField(queryset=Status.objects.all())
    type = PrimaryKeyRelatedField(queryset=Type.objects.all())
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = ['pk', 'date', 'status', 'type', 'category', 'subcategory', 'amount', 'description']
        depth = 2

    def validate(self, attrs):
        # Check if category and subcategory are of the same type
        attrs = super().validate(attrs)
        category = attrs['category']
        subcategory = attrs['subcategory']
        type = attrs['type']
        if category.type != type or subcategory.type != type:
            raise ValidationError('Category and subcategory must be of the same type')
        if category != subcategory.parent_category:
            raise ValidationError('Subcategory must be a child of category')
        return attrs


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ['pk', 'name']


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = ['pk', 'name']


class CategorySerializer(ModelSerializer):
    # Check if category and subcategory are of the same type
    type = PrimaryKeyRelatedField(queryset=Type.objects.all())
    parent_category = PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Category
        fields = ['pk', 'name', 'parent_category', 'type']
        depth = 1

    def validate(self, attrs):
        # Check if category and subcategory are of the same type
        attrs = super().validate(attrs)
        parent_category = attrs['parent_category']
        type = attrs['type']
        if parent_category.type != type:
            raise ValidationError('Parent category must be of the same type')
        return attrs
