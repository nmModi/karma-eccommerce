from django.contrib.auth import views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from .views import ResetPasswordView, RegisterView, ContactView, EmailFormView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', RegisterView.as_view(), name='register'),
    path('register/done/', TemplateView.as_view(template_name='account/register_done.html'), name='register_done'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('email/', EmailFormView.as_view(), name='send_mail'),
]
