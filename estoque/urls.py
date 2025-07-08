from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque_view, name='estoque'),
    path('produto/', views.produto_view, name='produto'),
    path('pedido/', views.pedido_view, name='pedido'),
]
