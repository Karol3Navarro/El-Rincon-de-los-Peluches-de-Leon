from django.db import models

# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='idCategoria', primary_key=True)
    categoria = models.CharField(max_length=20, blank=False, null=False)
    
    def __str__(self):
        return str(self.categoria)

class Peluche(models.Model):
    ESTADO_REVISION = [
        ('Sin Publicar', 'Sin Publicar'),
        ('Publicado', 'Publicado'),
        ('Vendido', 'Vendido'),
    ]

    id_peluche = models.AutoField(db_column='idPeluche', primary_key=True)
    nombre = models.CharField(max_length=20, blank=False, null=False)
    categoria = models.ForeignKey('categoria', on_delete=models.CASCADE, db_column='idCategoria')
    precio = models.CharField(max_length=20, null=True, blank=True)
    descripcion = models.TextField(default="Sin descripción")
    estado_revision = models.CharField(max_length=20, choices=ESTADO_REVISION, default='Sin Publicar')
    
    def __str__(self):
        return str(self.nombre)

class PelucheImagen(models.Model):
    peluche = models.ForeignKey(Peluche, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='peluches/')

#Para el numero de telefono. Temporal
class Configuracion(models.Model):
    telefono_whatsapp = models.CharField(
        max_length=20,
        help_text="Número de WhatsApp en formato internacional, sin + ni espacios"
    )

    def __str__(self):
        return f"Configuración principal ({self.telefono_whatsapp})"

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"