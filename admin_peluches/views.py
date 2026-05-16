from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Peluche, PelucheImagen, Configuracion
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.db.models import Count, Sum, Q
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from .forms import UserUpdateForm, ConfiguracionForm
from django.db.models.functions import TruncDate

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # tu vista principal
        else:
            return render(request, 'admin_peluches/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'admin_peluches/login.html')
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfil_view(request):
    user = request.user
    config = Configuracion.objects.first()

    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST, instance=user)
        config_form = ConfiguracionForm(request.POST, instance=config)
        password_form = PasswordChangeForm(user, request.POST)

        if "update_profile" in request.POST:
            if user_form.is_valid() and config_form.is_valid():
                user_form.save()
                config_form.save()
                messages.success(request, "Perfil actualizado ✅")
                return redirect('perfil')

        elif "change_password" in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # evita logout
                messages.success(request, "Contraseña actualizada 🔒")
                return redirect('perfil')

    else:
        user_form = UserUpdateForm(instance=user)
        config_form = ConfiguracionForm(instance=config)
        password_form = PasswordChangeForm(user)

    return render(request, 'admin_peluches/perfil.html', {
        'user_form': user_form,
        'config': config,
        'config_form': config_form,
        'password_form': password_form
    })

@login_required
def home(request):
    # Total de peluches por estado
    total_publicados = Peluche.objects.filter(estado_revision='Publicado').count()
    total_vendidos = Peluche.objects.filter(estado_revision='Vendido', entregado=True).count()
    
    # Ventas del día
    hoy = timezone.localdate()
    mes_actual = hoy.strftime("%Y-%m")

    ventas_dia = Peluche.objects.filter(estado_revision='Vendido',fecha_venta__date=hoy).count()
    ventas_dia_total = Peluche.objects.filter(estado_revision='Vendido', fecha_venta__date=hoy).aggregate(total=Sum('precio'))['total'] or 0

    inicio_mes = hoy.replace(day=1)
    ventas_mes = Peluche.objects.filter(estado_revision='Vendido', fecha_venta__isnull=False, fecha_venta__date__gte=inicio_mes, fecha_venta__date__lte=hoy).aggregate(total=Sum('precio'))['total'] or 0

    stock_disponible = Peluche.objects.filter(estado_revision__in=['Publicado', 'Sin Publicar']).count()
    
    entregas_pendientes = Peluche.objects.filter(estado_revision='Vendido', entregado=False).count() if hasattr(Peluche, 'entregado') else 0

    entregas_atrasadas = Peluche.objects.filter(
        estado_revision='Vendido',
        entregado=False,
        fecha_entrega__isnull=False,
        fecha_entrega__lt=timezone.now()
    ).count()
    
    context = {
        'total_publicados': total_publicados,
        'total_vendidos': total_vendidos,
        'entregas_pendientes': entregas_pendientes,
        'ventas_dia':ventas_dia,
        'ventas_dia_total': ventas_dia_total,
        'ventas_mes':ventas_mes,
        'stock_disponible':stock_disponible,
        'entregas_atrasadas':entregas_atrasadas,
        'mes_actual': mes_actual,
    }
    return render(request, 'admin_peluches/home.html', context)

#---Categoria
@login_required
def categoriaAdd(request):
    if request.method != "POST":
        categorias = Categoria.objects.all()
        context = {'categorias': categorias}
        return render(request, 'admin_peluches/categoria_add.html', context)

    else:
        categoria = request.POST["categoria"]
        Categoria.objects.create(categoria=categoria)

        categorias = Categoria.objects.all()

        context = {
            'categorias': categorias
        }

        return render(request, 'admin_peluches/categoria_add.html', context)
@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, id_categoria=pk)
    categoria.delete()
    messages.success(request, "Categoría eliminada correctamente 🗑️")
    return redirect('categoriaAdd')

#----Peluches----
@login_required
def peluches_list(request):
    # Obtener filtro desde GET
    estado_filtro = request.GET.getlist('estado')
    entrega_filtro = request.GET.get('entrega', 'Todos')
    tamano = request.GET.get('tamano')
    min_cm = request.GET.get('min_cm') or None
    max_cm = request.GET.get('max_cm') or None

    categoria_id = request.GET.getlist('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    
    query = request.GET.get('q')

    peluches = Peluche.objects.all().order_by('-id_peluche')

    # filtro por estado_filtro
    if estado_filtro:
        peluches = peluches.filter(estado_revision__in=estado_filtro)
    
    # filtro por entrega
    if entrega_filtro == 'pendiente':
        peluches = peluches.filter(entregado=False, estado_revision='Vendido')

    elif entrega_filtro == 'entregado':
        peluches = peluches.filter(entregado=True, estado_revision='Vendido')

    # Filtro por tamaño
    if tamano:
        peluches = peluches.filter(tamano=tamano)

    # 🔹 rango (alto en cm)
    if min_cm is not None and min_cm != "":
        min_cm = int(min_cm)
        peluches = peluches.filter(alto_cm__gte=min_cm)

    if max_cm is not None and max_cm != "":
        max_cm = int(max_cm)
        peluches = peluches.filter(alto_cm__lte=max_cm)

    #Categoria
    if categoria_id:
        peluches = peluches.filter(categoria_id__in=categoria_id)

    # PRECIO 🔥 NUEVO
    if precio_min:
        try:
            peluches = peluches.filter(precio__gte=int(precio_min.replace(".", "")))
        except ValueError:
            pass
    if precio_max:
        try:
            peluches = peluches.filter(precio__lte=int(precio_max.replace(".", "")))
        except ValueError:
            pass

    #Filtrar por búsqueda
    if query and query.strip():
        words = query.split()

        for word in words:
            peluches = peluches.filter(
                Q(nombre__icontains=word) |
                Q(descripcion__icontains=word) |
                Q(categoria__categoria__icontains=word) |
                Q(tamano__icontains=word) |
                Q(estado_revision__icontains=word)
            ).distinct()
    
    categorias = (
        Categoria.objects
        .annotate(
            total_peluches=Count(
                'peluche',
                filter=Q(peluche__estado_revision__in=['Publicado', 'Vendido'])
            )
        )
    )
    # Total filtrado
    total_peluches = peluches.count()
    # 🔥 PAGINACIÓN
    paginator = Paginator(peluches, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para llenar el dropdown de filtros
    estados = ['Todos'] + [choice[0] for choice in Peluche.ESTADO_REVISION]

    context = {
        'peluches': page_obj,
        'page_obj': page_obj,
        'total_peluches': total_peluches,
        'estados': estados,
        'tamanos': Peluche.TAMANOS,
        'tamano_seleccionado': tamano,
        'estado_seleccionado': estado_filtro,
        'entrega_seleccionado': entrega_filtro,
        'min_cm': min_cm or '',
        'max_cm': max_cm or '',
        'categorias': categorias,
        'filtro_categoria': categoria_id,
        'precio_min': precio_min or '',
        'precio_max': precio_max or '',
        'query': query,
    }
    return render(request, 'admin_peluches/peluches_list.html', context)

@login_required
def peluchesAdd(request):
    if request.method != "POST":
        categorias=Categoria.objects.all()
        context={'categorias':categorias, 'estado_choices': Peluche.ESTADO_REVISION}
        return render(request, 'admin_peluches/peluches_add.html', context)
    else:
        nombre=request.POST["nombre"]
        categoria = request.POST["categoria"]
        precio = request.POST.get("precio")
        precio = int(precio.replace(".", "")) if precio else None
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado_revision")
        imagenes = request.FILES.getlist("imagen")
        fecha_entrega = request.POST.get("fecha_entrega")
        lugar_entrega = request.POST.get("lugar_entrega")
        alto_cm = request.POST.get('alto_cm')   
        ancho_cm = request.POST.get('ancho_cm')
        alto_cm = int(alto_cm) if alto_cm else 0
        ancho_cm = int(ancho_cm) if ancho_cm else 0
        objCategoria= Categoria.objects.get(id_categoria= categoria)

        obj= Peluche.objects.create(
            nombre=nombre, 
            categoria=objCategoria, 
            precio=precio, 
            descripcion=descripcion, 
            estado_revision=estado,
            alto_cm=alto_cm,
            ancho_cm=ancho_cm)
        
        # 🆕 lógica de venta
        if estado == "Vendido" and not obj.fecha_venta:
            obj.fecha_venta = timezone.now()
            if fecha_entrega:
                obj.fecha_entrega = parse_datetime(fecha_entrega)
            obj.lugar_entrega = lugar_entrega
            obj.entregado = False  # queda pendiente
        else:
            # limpiar si no está vendido
            obj.fecha_venta = None
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
        
        messages.success(request, "Peluche agregado correctamente 🧸")

        return redirect('peluches_list')

@login_required
def peluches_del(request, pk):
    peluche = get_object_or_404(Peluche, id_peluche=pk)
    peluche.delete()

    messages.success(request, "Peluche eliminado correctamente 🗑️")

    return redirect('peluches_list')

#Eliminar Imagenes de Media/Peluches
@login_required
@receiver(post_delete, sender=PelucheImagen)
def eliminar_imagen(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)

@login_required
def peluches_findEdit(request, pk):
    if pk != "":
        peluche= Peluche.objects.get(id_peluche=pk)
        categorias=Categoria.objects.all()

        print(type(peluche.categoria.categoria))

        context={'peluche': peluche, 'categorias':categorias, 'estado_choices': Peluche.ESTADO_REVISION}
        if peluche:
            return render(request, 'admin_peluches/peluches_edit.html', context)
        else:
            return render(request, 'admin_peluches/peluches_list.html')
@login_required
def peluchesUpdate(request):
    if request.method == "POST":
        id_peluche = request.POST.get("id_peluche")
        nombre = request.POST["nombre"]
        categoria = request.POST["categoria"]
        precio = request.POST.get("precio")
        precio = int(precio.replace(".", "")) if precio else None
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado_revision")
        imagenes = request.FILES.getlist("imagenes")
        fecha_entrega = request.POST.get("fecha_entrega")
        lugar_entrega = request.POST.get("lugar_entrega")
        alto_cm = request.POST.get('alto_cm')   
        ancho_cm = request.POST.get('ancho_cm')
        alto_cm = int(alto_cm) if alto_cm else None
        ancho_cm = int(ancho_cm) if ancho_cm else None

        objCategoria = Categoria.objects.get(id_categoria=categoria)
        peluche = Peluche.objects.get(id_peluche=id_peluche)

        peluche.nombre = nombre
        peluche.categoria = objCategoria
        peluche.precio=precio
        peluche.descripcion=descripcion
        peluche.alto_cm= alto_cm
        peluche.ancho_cm= ancho_cm

        # 🆕 detectar cambio a vendido
        if estado == "Vendido" and peluche.estado_revision != "Vendido":
            peluche.fecha_venta = timezone.now()

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

        messages.success(request, "Peluche actualizado correctamente ✏️")
        return redirect('peluche', id_peluche=peluche.id_peluche)
    
@login_required
def peluche_imagen_del(request, id):
    img = PelucheImagen.objects.get(id=id)

    # eliminar archivo físico
    if img.imagen:
        if os.path.isfile(img.imagen.path):
            os.remove(img.imagen.path)

    peluche_id = img.peluche.id_peluche
    img.delete()
    messages.success(request, "Imagen eliminada correctamente 🖼️")
    return redirect('peluches_findEdit', pk=peluche_id)

@login_required
def peluche(request, id_peluche):
    peluche = get_object_or_404(Peluche, id_peluche=id_peluche)

    imagen_url = ""
    if peluche.imagenes.exists():
        imagen_url = request.build_absolute_uri(peluche.imagenes.first().imagen.url)

    context = {'peluche': peluche, 'imagen_url': imagen_url }
    return render(request, 'admin_peluches/peluche.html', context)

#---Calendario
@login_required
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
                "start": p.fecha_entrega.isoformat(),
                "description": p.lugar_entrega or "",
                "image": imagen_url,
            })

    return JsonResponse(eventos, safe=False)

@login_required
def calendario(request):
    return render(request, 'admin_peluches/calendario.html')

@login_required
def marcar_entregado(request, id):
    peluche = Peluche.objects.get(id_peluche=id)
    peluche.entregado = True
    peluche.save()

    return redirect('calendario')

#--Ventas--
@login_required
def ventas_reporte(request):
    hoy = timezone.localdate()
    periodo = request.GET.get('periodo', 'dia')

    ventas_qs = Peluche.objects.filter(
        estado_revision='Vendido',
        fecha_venta__isnull=False
    )

    if periodo == 'dia':
        ventas_qs = ventas_qs.filter(
            fecha_venta__date=hoy
        )

    elif periodo == 'semana':
        inicio = hoy - timedelta(days=hoy.weekday())  # lunes
        fin = inicio + timedelta(days=6)  # domingo

        ventas_qs = ventas_qs.filter(
            fecha_venta__date__gte=inicio,
            fecha_venta__date__lte=fin
        )

    elif periodo == 'mes':
        mes_param = request.GET.get('mes')

        if mes_param:
            # formato: YYYY-MM
            año, mes = map(int, mes_param.split('-'))
            inicio = date(año, mes, 1)

            if mes == 12:
                fin = date(año + 1, 1, 1) - timedelta(days=1)
            else:
                fin = date(año, mes + 1, 1) - timedelta(days=1)
        else:
            # fallback: mes actual
            inicio = hoy.replace(day=1)

            if hoy.month == 12:
                fin = hoy.replace(year=hoy.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                fin = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)

        ventas_qs = ventas_qs.filter(
            fecha_venta__date__gte=inicio,
            fecha_venta__date__lte=fin
        )

    elif periodo == 'todos':
        pass  # sin filtro adicional
    
    total_ganado = ventas_qs.aggregate(total=Sum('precio'))['total'] or 0
    context = {
        'ventas': ventas_qs,
        'total': ventas_qs.count(),
        'total_ganado': total_ganado,
        'periodo': periodo,
        'mes_seleccionado': request.GET.get('mes', ''),
    }

    return render(request, 'admin_peluches/ventas_reporte.html', context)