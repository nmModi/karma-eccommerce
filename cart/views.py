from django.shortcuts import redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product
from shop.recommender import Recommender
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.POST['productId']:
            action = request.POST['action']
            if action == 'add':
                cart.add(product=product)
            else:
                cart.add(product=product,
                         quantity=-1)
    except MultiValueDictKeyError:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class CartView(TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data()
        context['coupon_apply_form'] = CouponApplyForm()
        cart = Cart(self.request)
        context['cart'] = cart
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'],
                         'update': True})
        cart_products = [item['product'] for item in cart]
        r = Recommender()
        if len(cart_products) > 0:
            context['recommended_products'] = r.suggest_products_for(cart_products, max_results=8)
        else:
            context['recommended_products'] = None
        return context
