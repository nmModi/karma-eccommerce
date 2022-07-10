from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('filter_data/', views.FilterData.as_view(), name='filter_data'),
    path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('load_more/', views.LoadMoreColors.as_view(), name='load_more')
]
