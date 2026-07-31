from django.contrib import admin
from admintheme_sandbox.admin.import_export import AdminThemeSandboxModelAdmin as DSGovBrModelAdmin
from .models import Evento, InscricaoEvento
from django.db import models
from django import forms


@admin.register(Evento)
class EventoAdmin(DSGovBrModelAdmin):
    list_display = ("titulo", "data_inicio", "data_fim", "local", "vagas", "preco")
    list_filter = ("data_inicio", "local")
    search_fields = ("titulo", "descricao", "local")


@admin.register(InscricaoEvento)
class InscricaoEventoAdmin(DSGovBrModelAdmin):
    list_display = (
        "nome_participante",
        "evento",
        "data_inscricao",
        "pago",
        "valor_pago",
    )
    list_filter = ("pago", "evento", "data_inscricao")
    search_fields = ("nome_participante", "email_participante")
    date_hierarchy = "data_inscricao"

    # Exemplo de formfield_overrides para validação visual
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 3, "class": "vLargeTextField"})
        },
    }
