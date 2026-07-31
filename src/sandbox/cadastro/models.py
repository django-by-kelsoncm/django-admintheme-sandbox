from django.db import models


class Orgao(models.Model):
    nome = models.CharField("Nome do Órgão", max_length=255)
    sigla = models.CharField("Sigla", max_length=20)
    descricao = models.TextField("Descrição", blank=True, null=True)
    data_criacao = models.DateField("Data de Criação", blank=True, null=True)
    ativo = models.BooleanField("Está Ativo?", default=True)

    class Meta:
        verbose_name = "Órgão"
        verbose_name_plural = "Órgãos"

    def __str__(self):
        return f"{self.sigla} - {self.nome}"


class Servidor(models.Model):
    orgao = models.ForeignKey(
        Orgao,
        on_delete=models.CASCADE,
        verbose_name="Órgão Vinculado",
        related_name="servidores",
    )
    nome = models.CharField("Nome Completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14, help_text="Formato: 000.000.000-00")
    email = models.EmailField("E-mail Funcional")
    cargo = models.CharField("Cargo Ocupado", max_length=150)
    data_admissao = models.DateField("Data de Admissão")

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"

    def __str__(self):
        return self.nome


class Documento(models.Model):
    TIPOS_DOCUMENTO = [
        ("identidade", "Documento de Identidade"),
        ("diploma", "Diploma Acadêmico"),
        ("portaria", "Portaria de Nomeação"),
        ("outros", "Outros"),
    ]
    servidor = models.ForeignKey(
        Servidor,
        on_delete=models.CASCADE,
        verbose_name="Servidor",
        related_name="documentos",
    )
    tipo = models.CharField("Tipo de Documento", max_length=30, choices=TIPOS_DOCUMENTO)
    arquivo = models.FileField(
        "Arquivo PDF/Imagem", upload_to="documentos/", blank=True, null=True
    )
    data_upload = models.DateTimeField("Data do Upload", auto_now_add=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.servidor.nome}"


class Servico(models.Model):
    nome = models.CharField("Nome do Serviço", max_length=255)
    url_portal = models.URLField("URL no Portal gov.br", blank=True, null=True)
    publico_alvo = models.CharField(
        "Público-Alvo", max_length=200, help_text="Ex: Cidadãos, Empresas, Servidores"
    )
    orgaos_envolvidos = models.ManyToManyField(
        Orgao, verbose_name="Órgãos Envolvidos", related_name="servicos"
    )

    class Meta:
        verbose_name = "Serviço Público"
        verbose_name_plural = "Serviços Públicos"

    def __str__(self):
        return self.nome
