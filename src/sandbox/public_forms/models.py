from django.db import models


class SolicitacaoServico(models.Model):
    TIPOS_SOLICITACAO = [
        ("reclamacao", "Reclamação"),
        ("sugestao", "Sugestão"),
        ("elogio", "Elogio"),
        ("duvida", "Dúvida"),
    ]
    nome = models.CharField("Nome Completo", max_length=255)
    email = models.EmailField("E-mail para Contato")
    telefone = models.CharField(
        "Telefone Celular", max_length=20, help_text="Ex: (61) 99999-9999"
    )
    tipo = models.CharField(
        "Tipo de Solicitação", max_length=20, choices=TIPOS_SOLICITACAO
    )
    descricao = models.TextField(
        "Descrição Detalhada",
        help_text="Escreva em detalhes a sua solicitação ou manifestação.",
    )
    anexo = models.FileField(
        "Arquivo de Anexo", upload_to="solicitacoes/", blank=True, null=True
    )
    concorda_termos = models.BooleanField(
        "Concordo com os Termos de Uso e LGPD", default=False
    )
    status_interno = models.CharField(
        "Status Interno (Hidden)", max_length=20, default="novo"
    )
    data_criacao = models.DateTimeField("Data de Criação", auto_now_add=True)

    class Meta:
        verbose_name = "Solicitação de Serviço"
        verbose_name_plural = "Solicitações de Serviço"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"
