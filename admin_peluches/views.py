from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Peluche, PelucheImagen
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.utils import timezone
from django.db.models import Count
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

# Create your views here.

def home(request):
    # Total de peluches por estado
    total_publicados = Peluche.objects.filter(estado_revision='Publicado').count()
    total_vendidos = Peluche.objects.filter(estado_revision='Vendido', entregado=True).count()
    
    # Ventas del día (suponiendo que la fecha de venta sea cuando se pone 'Vendido')
    # Necesitarías un campo 'fecha_venta' en tu modelo Peluche para esto
    hoy = timezone.now().date()
    ventas_dia = Peluche.objects.filter(estado_revision='Vendido', fecha_venta=hoy).count() if hasattr(Peluche, 'fecha_venta') else 0
    
    # Entregas pendientes (opcional, necesitas un campo 'entregado' booleano)
    entregas_pendientes = Peluche.objects.filter(estado_revision='Vendido', entregado=False).count() if hasattr(Peluche, 'entregado') else 0

    context = {
        'total_publicados': total_publicados,
        'total_vendidos': total_vendidos,
        'entregas_pendientes': entregas_pendientes
    }
    return render(request, 'admin_peluches/home.html', context)

def categoriaAdd(request):
    if request.method != "POST":
        categorias = Categoria.objects.all()
        context={'categorias':categorias}
        return render(request, 'admin_peluches/categoria_add.html', context)
    else:
        categoria=request.POST["categoria"]
        obj= Categoria.objects.create(categoria=categoria)
        obj.save()

        context={'mensaje':"Ok, categoria grabada"}
        return render(request, 'admin_peluches/categoria_add.html', context)

#----Peluches----
def peluches_list(request):
    # Obtener filtro desde GET
    estado_filtro = request.GET.get('estado', 'Todos')  # default = Todos
    entrega_filtro = request.GET.get('entrega', 'Todos')
    peluches = Peluche.objects.all()

    # filtro por estado
    if estado_filtro != 'Todos':
        peluches = peluches.filter(estado_revision=estado_filtro)
    
    # filtro por entrega (solo aplica si está vendido normalmente)
    if entrega_filtro == 'pendiente':
        peluches = peluches.filter(entregado=False, estado_revision='Vendido')

    elif entrega_filtro == 'entregado':
        peluches = peluches.filter(entregado=True, estado_revision='Vendido')

    # Para llenar el dropdown de filtros
    estados = ['Todos'] + [choice[0] for choice in Peluche.ESTADO_REVISION]
    
    context = {
        'peluches': peluches,
        'estados': estados,
        'estado_seleccionado': estado_filtro,
        'entrega_seleccionado': entrega_filtro,
    }
    return render(request, 'admin_peluches/peluches_list.html', context)

def peluchesAdd(request):
    if request.method != "POST":
        categorias=Categoria.objects.all()
        context={'categorias':categorias, 'estado_choices': Peluche.ESTADO_REVISION}
        return render(request, 'admin_peluches/peluches_add.html', context)
    else:
        nombre=request.POST["nombre"]
        categoria = request.POST["categoria"]
        precio = request.POST.get("precio")
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado_revision")
        imagenes = request.FILES.getlist("imagen")
        fecha_entrega = request.POST.get("fecha_entrega")
        lugar_entrega = request.POST.get("lugar_entrega")
        objCategoria= Categoria.objects.get(id_categoria= categoria)


        obj= Peluche.objects.create(
            nombre=nombre, 
            categoria=objCategoria, 
            precio=precio, 
            descripcion=descripcion, 
            estado_revision=estado)
        
        # 🆕 lógica de entrega
        if estado == "Vendido":
            if fecha_entrega:
                obj.fecha_entrega = parse_datetime(fecha_entrega)
            obj.lugar_entrega = lugar_entrega
            obj.entregado = False  # queda pendiente
        else:
            # limpiar si no está vendido
            obj.fecha_entrega = None
            obj.lugar_entrega = None
            obj.entregado = False
        
        obj.save()
        # Guardar múltiples imágenes
        for img in imagenes:
            PelucheImagen.objects.create(
                peluche=obj,
                imagen=img
            )
        
        context={'mensaje':"Ok, datos grabados"}
        return render(request, 'admin_peluches/peluches_add.html', context)

def peluches_del(request,pk):
    context={}
    try:
        peluche= Peluche.objects.get(id_peluche=pk)

        peluche.delete()
        mensaje="Bien, datos eliminados"
        peluches = Peluche.objects.all()
        context = {'peluches' : peluches, 'mensaje':mensaje}
        return render(request, 'admin_peluches/peluches_list.html', context)
    except:
        mensaje="Error, Peluche no existe"
        peluches = Peluche.objects.all()
        context= {'peluches': peluches, 'mensaje':mensaje}
        return render(request, 'admin_peluches/peluches_list.html', context)

#Eliminar Imagenes de Media/Peluches
@receiver(post_delete, sender=PelucheImagen)
def eliminar_imagen(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)

def peluches_findEdit(request, pk):
    if pk != "":
        peluche= Peluche.objects.get(id_peluche=pk)
        categorias=Categoria.objects.all()

        print(type(peluche.categoria.categoria))

        context={'peluche': peluche, 'categorias':categorias, 'estado_choices': Peluche.ESTADO_REVISION}
        if peluche:
            return render(request, 'admin_peluches/peluches_edit.html', context)
        else:
            context={'mensaje':"Error, peluche no existe"}
            return render(request, 'admin_peluches/peluches_list.html', context)

def peluchesUpdate(request):
    if request.method == "POST":
        id_peluche = request.POST.get("id_peluche")
        nombre = request.POST["nombre"]
        categoria = request.POST["categoria"]
        precio = request.POST.get("precio")
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado_revision")
        imagenes = request.FILES.getlist("imagenes")
        fecha_entrega = request.POST.get("fecha_entrega")
        lugar_entrega = request.POST.get("lugar_entrega")

        objCategoria = Categoria.objects.get(id_categoria=categoria)
        peluche = Peluche.objects.get(id_peluche=id_peluche)

        peluche.nombre = nombre
        peluche.categoria = objCategoria
        peluche.precio=precio
        peluche.descripcion=descripcion
        peluche.estado_revision=estado

        # 🆕 lógica de entrega
        if estado == "Vendido":
            if fecha_entrega:
                peluche.fecha_entrega = parse_datetime(fecha_entrega)
            peluche.lugar_entrega = lugar_entrega
            peluche.entregado = False  # queda pendiente
        else:
            # limpiar si no está vendido
            peluche.fecha_entrega = None
            peluche.lugar_entrega = None
            peluche.entregado = False

        peluche.save()

        for img in imagenes:
            PelucheImagen.objects.create(peluche=peluche, imagen=img)

        categorias = Categoria.objects.all()
        return redirect('peluche', id_peluche=peluche.id_peluche)

def peluche_imagen_del(request, id):
    img = PelucheImagen.objects.get(id=id)

    # eliminar archivo físico
    if img.imagen:
        if os.path.isfile(img.imagen.path):
            os.remove(img.imagen.path)

    peluche_id = img.peluche.id_peluche
    img.delete()

    return redirect('peluches_findEdit', pk=peluche_id)

def peluche(request, id_peluche):
    peluche = get_object_or_404(Peluche, id_peluche=id_peluche)

    imagen_url = ""
    if peluche.imagenes.exists():
        imagen_url = request.build_absolute_uri(peluche.imagenes.first().imagen.url)

    context = {'peluche': peluche, 'imagen_url': imagen_url }
    return render(request, 'admin_peluches/peluche.html', context)

#---Calendario
def eventos_entrega(request):
    peluches = Peluche.objects.filter(fecha_entrega__isnull=False, entregado=False)

    eventos = []
    for p in peluches:
        if p.fecha_entrega:
            imagen_url = ""
            primera_img = p.imagenes.first()
            if primera_img:
                imagen_url = primera_img.imagen.url

            eventos.append({
                "id": p.id_peluche,
                "title": p.nombre,
                "start": p.fecha_entrega.strftime("%Y-%m-%dT%H:%M:%S"),
                "description": p.lugar_entrega or "",
                "image": imagen_url,
            })

    return JsonResponse(eventos, safe=False)

def calendario(request):
    return render(request, 'admin_peluches/calendario.html')

def marcar_entregado(request, id):
    peluche = Peluche.objects.get(id_peluche=id)
    peluche.entregado = True
    peluche.save()

    return redirect('calendario')