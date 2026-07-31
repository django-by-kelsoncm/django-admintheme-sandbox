from django.db import models


class Midia(models.Model):
    titulo = models.CharField("Título da Mídia", max_length=150)
    arquivo = models.FileField(
        "Arquivo Anexo", upload_to="biblioteca/arquivos/", blank=True, null=True
    )
    imagem = models.ImageField(
        "Imagem", upload_to="biblioteca/imagens/", blank=True, null=True
    )
    descricao = models.TextField("Descrição Breve", blank=True, null=True)
    data_upload = models.DateTimeField("Data do Upload", auto_now_add=True)

    class Meta:
        verbose_name = "Arquivo de Mídia"
        verbose_name_plural = "Arquivos de Mídia"

    def __str__(self):
        return self.titulo
