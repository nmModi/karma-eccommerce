from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.PaymentDoneView.as_view(), name='done'),
    path('canceled/', views.PaymentCanceledView.as_view(), name='canceled'),
]
