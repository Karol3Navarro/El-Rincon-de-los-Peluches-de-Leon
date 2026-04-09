from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('peluches',views.peluches, name='peluches'),
    path('peluches_vendidos',views.peluches_vendidos, name='peluches_vendidos'),
    path('peluche/<int:id_peluche>/',views.ver_peluche, name='ver_peluche')
]