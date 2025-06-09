from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class EntradaBlog(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blog/')
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Entrada de Blog"
        verbose_name_plural = "Entradas de Blog"

    def __str__(self):
        return self.titulo
