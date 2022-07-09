from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView

from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created
from coupons.forms import CouponApplyForm


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear cart
            cart.clear()
            order_created.delay(order.id)
            # save order in session
            request.session['order_id'] = order.id
            # redirect to payment page
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        coupon_apply_form = CouponApplyForm()
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form, 'coupon_apply_form': coupon_apply_form})


class ConfirmationView(TemplateView):
    template_name = 'orders/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            context['orders'] = Order.objects.filter(user=self.request.user, paid=True).order_by('-updated')
        except TypeError:
            messages.error(self.request, 'You are not authorized')
        return context
