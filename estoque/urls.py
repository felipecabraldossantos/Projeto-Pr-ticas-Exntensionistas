from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='estoque/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('estoque/', views.estoque_view, name='estoque'),
    path('produto/', views.produto_view, name='produto'),
    path('pedido/', views.pedido_view, name='pedido'),
    path('produto/editar/<int:produto_id>/', views.editar_produto_view, name='editar_produto'),
    path('produto/editar/', views.editar_produto_redirect_view, name='editar_produto_redirect'),
    path('pedido/editar/<int:pedido_id>/', views.editar_pedido_view, name='editar_pedido'),
    path('contato/', views.contato, name='contato'),
    path('contato/enviado/', views.contato_enviado, name='contato_enviado'),
]
