from django.db import models


class Categoria(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100)
    slug = models.SlugField("Slug", max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Tag(models.Model):
    nome = models.CharField("Nome da Tag", max_length=50, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.nome


class Noticia(models.Model):
    STATUS_CHOICES = [
        ("rascunho", "Rascunho"),
        ("publicado", "Publicado"),
        ("arquivado", "Arquivado"),
    ]
    titulo = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=200, unique=True)
    conteudo = models.TextField("Conteúdo")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, verbose_name="Categoria"
    )
    tags = models.ManyToManyField(Tag, verbose_name="Tags", blank=True)
    status = models.CharField(
        "Status", max_length=15, choices=STATUS_CHOICES, default="rascunho"
    )
    data_publicacao = models.DateTimeField("Data de Publicação", blank=True, null=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE,
        verbose_name="Notícia",
        related_name="comentarios",
    )
    autor = models.CharField("Autor", max_length=100)
    comentario = models.TextField("Comentário")
    aprovado = models.BooleanField("Aprovado?", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Comentário de Notícia"
        verbose_name_plural = "Comentários de Notícias"

    def __str__(self):
        return f"{self.autor} em '{self.noticia.titulo}'"
