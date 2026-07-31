from django.db import models
from django.conf import settings


class Chamado(models.Model):
    PRIORIDADE_CHOICES = [
        ("baixa", "Baixa"),
        ("media", "Média"),
        ("alta", "Alta"),
    ]
    STATUS_CHOICES = [
        ("novo", "Novo"),
        ("em_atendimento", "Em Atendimento"),
        ("resolvido", "Resolvido"),
        ("fechado", "Fechado"),
    ]
    protocolo = models.CharField("Nº Protocolo", max_length=20, unique=True)
    assunto = models.CharField("Assunto", max_length=200)
    descricao = models.TextField("Descrição do Problema")
    prioridade = models.CharField(
        "Prioridade", max_length=10, choices=PRIORIDADE_CHOICES, default="media"
    )
    status = models.CharField(
        "Status", max_length=20, choices=STATUS_CHOICES, default="novo"
    )
    atendente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Atendente Responsável",
    )
    resposta = models.TextField("Resposta do Atendimento", blank=True, null=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    resolvido_em = models.DateTimeField("Resolvido em", blank=True, null=True)

    class Meta:
        verbose_name = "Chamado de Suporte"
        verbose_name_plural = "Chamados de Suporte"

    def __str__(self):
        return f"{self.protocolo} - {self.assunto}"
