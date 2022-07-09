from collections import Counter

from .models import Product
from orders.models import OrderItem


class ProductFilter:
    def get_all_products(self):
        return Product.objects.filter(available=True).select_related('brand').order_by('-created')

    def get_best_seller(self):
        lst = []
        for i in OrderItem.objects.all().select_related('product'):
            lst.append(i.product)
        return Counter(lst)
