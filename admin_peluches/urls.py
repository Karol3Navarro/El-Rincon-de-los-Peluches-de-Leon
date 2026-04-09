from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('crud', views.crud, name= 'crud'),
    path('categoriaAdd', views.categoriaAdd, name= 'categoriaAdd'),
    path('peluchesAdd', views.peluchesAdd, name= 'peluchesAdd'),
    path('peluches_del/<str:pk>', views.peluches_del, name='peluches_del'),
    path('peluches_findEdit/<str:pk>', views.peluches_findEdit, name='peluches_findEdit'),
    path('peluchesUpdate', views.peluchesUpdate, name='peluchesUpdate'),
    path('peluche_imagen_del/<int:id>/', views.peluche_imagen_del, name='peluche_imagen_del'),
]