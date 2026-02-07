from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    bio = models.TextField(max_length=500, blank=True, default="")
    foto = models.ImageField(upload_to="fotos_perfil/", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(User, related_name="curtidas", blank=True)

    def __str__(self):
        return f"{self.autor} - {self.texto[:20]}..."

    def total_curtidas(self):
        return self.curtidas.count()


class Seguidor(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seguindo")
    seguindo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seguidores")

    class Meta:
        unique_together = ('seguidor', 'seguindo')

    def __str__(self):
        return f"{self.seguidor} segue {self.seguindo}"


class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.autor}"
