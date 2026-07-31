from django import forms
from .models import SolicitacaoServico


class SolicitacaoModelForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoServico
        fields = [
            "nome",
            "email",
            "telefone",
            "tipo",
            "descricao",
            "anexo",
            "concorda_termos",
            "status_interno",
        ]
        widgets = {
            "status_interno": forms.HiddenInput(),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone")
        if len(telefone) < 10:
            raise forms.ValidationError(
                "O telefone deve ter pelo menos 10 dígitos, incluindo o DDD."
            )
        return telefone

    def clean(self):
        cleaned_data = super().clean()
        concorda = cleaned_data.get("concorda_termos")
        if not concorda:
            raise forms.ValidationError(
                "Você precisa aceitar os termos de LGPD e Uso para enviar a solicitação."
            )
        return cleaned_data
