from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('home', views.home, name='home'),
    path('peluches_list', views.peluches_list, name= 'peluches_list'),
    path('categoriaAdd', views.categoriaAdd, name= 'categoriaAdd'),
    path('categoria/delete/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    path('peluchesAdd', views.peluchesAdd, name= 'peluchesAdd'),
    path('peluches_del/<str:pk>', views.peluches_del, name='peluches_del'),
    path('peluches_findEdit/<str:pk>', views.peluches_findEdit, name='peluches_findEdit'),
    path('peluchesUpdate', views.peluchesUpdate, name='peluchesUpdate'),
    path('peluche_imagen_del/<int:id>/', views.peluche_imagen_del, name='peluche_imagen_del'),
    path('peluche/<int:id_peluche>/', views.peluche, name='peluche'),
    path('calendario/', views.calendario, name='calendario'),
    path('eventos/', views.eventos_entrega, name='eventos_entrega'),
    path('entregado/<int:id>/', views.marcar_entregado, name='marcar_entregado'),
    path('ventas/', views.ventas_reporte, name='ventas_reporte'),
]