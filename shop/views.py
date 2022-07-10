from django.contrib import messages
from django.db.models import Q, Min, Max
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from .forms import CommentForm
from .models import *
from .recommender import Recommender
from .utils import ProductFilter
from cart.forms import CartAddProductForm


class HomeView(ProductFilter, TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(active=True).select_related('product').order_by('-id')
        context['cart_product_form'] = CartAddProductForm()
        context['brands'] = Brand.objects.all()[:5]
        return context


class ProductListView(ProductFilter, ListView):
    model = Product
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        return self.get_all_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['cart_product_form'] = CartAddProductForm()
        context['categories'] = Category.objects.distinct().values_list('name', 'id')
        context['brands'] = Brand.objects.all().values_list('name', 'id')
        context['colors'] = Color.objects.all().values_list('name', 'id', 'color_code')[:2]
        context['minMaxPrice'] = Product.objects.aggregate(Min('price'), Max('price'))
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_product_form'] = CartAddProductForm()
        product = kwargs['object']
        r = Recommender()
        context['recommended_products'] = r.suggest_products_for([product], 8)
        return context


class SearchView(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        q = self.request.GET['q']
        queryset = Product.objects.filter(Q(brand__name__icontains=q) | Q(model__icontains=q), available=True)
        if queryset:
            messages.success(self.request, f'Search results for {q}...')
        else:
            messages.error(self.request, 'No such products')
        return queryset


class FilterData(View):
    def get(self, request):
        colors = request.GET.getlist('color[]')
        brands = request.GET.getlist('brand[]')
        categories = request.GET.getlist('category[]')
        min_price = request.GET['minPrice']
        max_price = request.GET['maxPrice']
        ordering = request.GET['ordering']
        seasons = request.GET['seasons']
        all_products = Product.objects.filter(available=True).order_by(ordering)
        if seasons != 'all':
            all_products = all_products.filter(season=seasons)
        all_products = all_products.filter(price__gte=min_price)
        all_products = all_products.filter(price__lte=max_price)
        if len(colors) > 0:
            all_products = all_products.filter(color__id__in=colors).distinct()
        if len(brands) > 0:
            all_products = all_products.filter(brand__id__in=brands)
        if len(categories) > 0:
            all_products = all_products.filter(category__id__in=categories)
        t = render_to_string('shop/ajax/product-list.html', {'data': all_products})
        return JsonResponse({'data': t})


class LoadMoreColors(View):
    def get(self, request):
        colors = Color.objects.all().values_list('name', 'id', 'color_code')
        t = render_to_string('shop/ajax/load_more.html', {'colors': colors})
        return JsonResponse({'colors': t})


class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())
