from .models import Product, Category
from modeltranslation.translator import TranslationOptions, register
from modeltranslation.admin import TranslationAdmin


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')
