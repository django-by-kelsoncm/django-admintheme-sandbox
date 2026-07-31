from django.db import models


class Evento(models.Model):
    titulo = models.CharField("Título do Evento", max_length=200)
    descricao = models.TextField("Descrição")
    data_inicio = models.DateField("Data de Início")
    data_fim = models.DateField("Data de Término")
    local = models.CharField("Local", max_length=200)
    vagas = models.PositiveIntegerField("Total de Vagas")
    preco = models.DecimalField(
        "Preço da Inscrição", max_digits=10, decimal_places=2, default=0.00
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.titulo


class InscricaoEvento(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        verbose_name="Evento Selecionado",
        related_name="inscricoes",
    )
    nome_participante = models.CharField("Nome do Participante", max_length=255)
    email_participante = models.EmailField("E-mail do Participante")
    data_inscricao = models.DateTimeField("Data da Inscrição", auto_now_add=True)
    pago = models.BooleanField("Inscrição Paga?", default=False)
    valor_pago = models.DecimalField(
        "Valor Pago", max_digits=10, decimal_places=2, default=0.00
    )

    class Meta:
        verbose_name = "Inscrição em Evento"
        verbose_name_plural = "Inscrições em Eventos"

    def __str__(self):
        return f"{self.nome_participante} em {self.evento.titulo}"
