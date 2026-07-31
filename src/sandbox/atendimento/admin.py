from django.contrib import admin
from admintheme_sandbox.admin.import_export import AdminThemeSandboxModelAdmin as DSGovBrModelAdmin
from .models import Chamado


@admin.register(Chamado)
class ChamadoAdmin(DSGovBrModelAdmin):
    list_display = (
        "protocolo",
        "assunto",
        "prioridade",
        "status",
        "atendente",
        "criado_em",
    )
    list_filter = ("prioridade", "status", "criado_em")
    search_fields = ("protocolo", "assunto", "descricao", "resposta")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.status in ["resolvido", "fechado"]:
                return [
                    "protocolo",
                    "assunto",
                    "descricao",
                    "prioridade",
                    "criado_em",
                    "resolvido_em",
                ]
            return ["protocolo", "criado_em", "resolvido_em"]
        return ["protocolo", "criado_em", "resolvido_em"]

    def save_model(self, request, obj, form, change):
        if not change:
            import datetime
            import random

            obj.protocolo = f"CH-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        super().save_model(request, obj, form, change)
