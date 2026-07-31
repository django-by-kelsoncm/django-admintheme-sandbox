from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.core.management import call_command


def is_staff(user):
    return user.is_active and user.is_staff


def panel_view(request):
    User = get_user_model()
    users = User.objects.filter(
        username__in=[
            "superuser",
            "staff_admin_total",
            "staff_editorial_full",
            "staff_editorial_readonly",
            "staff_atendimento_sem_delete",
            "staff_eventos_sem_add",
            "staff_cadastro_view_only",
            "user_autenticado_comum",
            "user_inativo",
        ]
    )
    return render(
        request,
        "qa_orchestrator/panel.html",
        {"title": "Orquestrador de QA", "users": users, "current_user": request.user},
    )


def login_as_view(request, username):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
        # Força autenticação sem senha para testes rápidos de QA
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        messages.success(request, f"Autenticado com sucesso como: {username}")
    except User.DoesNotExist:
        messages.error(
            request,
            f"Usuário '{username}' não encontrado. Por favor, execute o Seed do Banco.",
        )
    return redirect("qa_orchestrator:panel")


def reset_db_view(request):
    try:
        call_command("seed_sandbox")
        messages.success(
            request, "Banco de dados reinicializado e semeado com sucesso!"
        )
    except Exception as e:
        messages.error(request, f"Erro ao reiniciar banco de dados: {str(e)}")
    return redirect("qa_orchestrator:panel")
