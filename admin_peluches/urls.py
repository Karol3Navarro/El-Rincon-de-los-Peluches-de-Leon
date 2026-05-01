from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('', views.home, name='home'),
    path('peluches/', views.peluches_list, name= 'peluches_list'),
    path('categoria/agregar/', views.categoriaAdd, name= 'categoriaAdd'),
    path('categoria/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    path('peluches/agregar/', views.peluchesAdd, name= 'peluchesAdd'),
    path('peluches/eliminar/<str:pk>', views.peluches_del, name='peluches_del'),
    path('peluches_findEdit/<str:pk>', views.peluches_findEdit, name='peluches_findEdit'),
    path('peluches/editar/', views.peluchesUpdate, name='peluchesUpdate'),
    path('peluche_imagen_del/<int:id>/', views.peluche_imagen_del, name='peluche_imagen_del'),
    path('peluche/<int:id_peluche>/', views.peluche, name='peluche'),
    path('calendario/', views.calendario, name='calendario'),
    path('eventos/', views.eventos_entrega, name='eventos_entrega'),
    path('entregado/<int:id>/', views.marcar_entregado, name='marcar_entregado'),
    path('reporte-ventas/', views.ventas_reporte, name='ventas_reporte'),
]