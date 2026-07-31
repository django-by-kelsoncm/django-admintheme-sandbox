from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Instruções do Sandbox - DSGovBR"
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard do Sandbox - DSGovBR"
        context["apps"] = [
            {
                "name": "Cadastro Institucional (Admin)",
                "url": "/admin/cadastro/",
                "desc": "Validação de listagem, inlines, autocomplete, filtros, etc.",
            },
            {
                "name": "Editorial (Admin)",
                "url": "/admin/editorial/",
                "desc": "Validação de Many-to-Many, pre-populated slugs, tabular inlines.",
            },
            {
                "name": "Atendimento & Chamados (Admin)",
                "url": "/admin/atendimento/",
                "desc": "Validação de permissões a nível de modelo e readonly_fields.",
            },
            {
                "name": "Eventos & Inscrições (Admin)",
                "url": "/admin/eventos/",
                "desc": "Validação de date_hierarchy e formfield_overrides.",
            },
            {
                "name": "Autenticação & Contas (Auth)",
                "url": "/admin/",
                "desc": "Validação visual do fluxo de Login/Logout, reset e alteração de senha.",
            },
            {
                "name": "Formulários Públicos (Public Forms)",
                "url": "/forms/",
                "desc": "Validação de inputs puros Django (as_p, as_ul, as_div e manual).",
            },
            {
                "name": "Showcase UI (Componentes)",
                "url": "/showcase/",
                "desc": "Exibição de todos os componentes puros do DS GovBR.",
            },
            {
                "name": "QA Orchestrator (Painel de Teste)",
                "url": "/qa/",
                "desc": "Utilitários para simular perfis de acesso, resetar dados e massas.",
            },
        ]
        return context


class SiteSearchView(TemplateView):
    template_name = "core/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["query"] = query
        context["title"] = f"Pesquisa: {query}" if query else "Pesquisa"

        from django.db import models
        from cadastro.models import Orgao, Servidor, Servico

        orgaos = []
        servidores = []
        servicos = []

        if query:
            orgaos = Orgao.objects.filter(
                models.Q(nome__icontains=query) | models.Q(sigla__icontains=query)
            )
            servidores = Servidor.objects.filter(
                models.Q(nome__icontains=query) | models.Q(cargo__icontains=query)
            )
            servicos = Servico.objects.filter(
                models.Q(nome__icontains=query)
                | models.Q(publico_alvo__icontains=query)
            )

        total_results = len(orgaos) + len(servidores) + len(servicos)

        context["results"] = {
            "orgaos": orgaos,
            "servidores": servidores,
            "servicos": servicos,
            "count": total_results,
        }
        return context


def site_index_autocomplete(request):
    from django.db import models
    from django.http import JsonResponse
    from cadastro.models import Orgao, Servidor, Servico

    query = request.GET.get("q", "").strip()
    results = []
    if len(query) >= 2:
        for obj in Orgao.objects.filter(
            models.Q(nome__icontains=query) | models.Q(sigla__icontains=query)
        )[:5]:
            results.append(obj.nome)
            results.append(obj.sigla)
        for obj in Servidor.objects.filter(nome__icontains=query)[:5]:
            results.append(obj.nome)
        for obj in Servico.objects.filter(nome__icontains=query)[:5]:
            results.append(obj.nome)

    results = list(sorted(set(results)))[:10]
    return JsonResponse(results, safe=False)
