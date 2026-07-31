from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    cargo = models.CharField("Cargo Ocupado", max_length=150, blank=True, null=True)
    orgao = models.ForeignKey(
        "cadastro.Orgao",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Órgão Vinculado",
    )

    class Meta:
        verbose_name = "Usuário Customizado"
        verbose_name_plural = "Usuários Customizados"
