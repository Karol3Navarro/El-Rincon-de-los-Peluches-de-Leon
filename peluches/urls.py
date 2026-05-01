from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.index, name='index'),
    path('productos',views.peluches, name='peluches'),
    path('producto/<int:id_peluche>/',views.ver_peluche, name='ver_peluche')
]