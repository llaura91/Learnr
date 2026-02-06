from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(User, related_name="curtidas", blank=True)

    def total_curtidas(self):
        return self.curtidas.count()

    def __str__(self):
        return f"{self.autor} - {self.texto[:20]}..."
