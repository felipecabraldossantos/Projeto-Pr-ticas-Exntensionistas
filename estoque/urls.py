from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque_view, name='estoque'),
    path('produto/', views.produto_view, name='produto'),
    path('pedido/', views.pedido_view, name='pedido'),
    path('produto/editar/<int:produto_id>/', views.editar_produto_view, name='editar_produto'),
    path('produto/editar/', views.editar_produto_redirect_view, name='editar_produto_redirect'),
]
