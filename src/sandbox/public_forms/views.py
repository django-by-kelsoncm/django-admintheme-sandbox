from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib import messages
from .forms import SolicitacaoModelForm


class PublicFormDemoView(CreateView):
    template_name = "public_forms/form_demo.html"
    form_class = SolicitacaoModelForm
    success_url = "/forms/sucesso/"

    def form_valid(self, form):
        messages.success(self.request, "Solicitação enviada com sucesso!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = self.request.GET.get("mode", "manual")
        return context


def sucesso_view(request):
    return render(request, "public_forms/sucesso.html", {"title": "Sucesso!"})
