from django.urls import path
from .views import panel_view, login_as_view, reset_db_view

app_name = "qa_orchestrator"

urlpatterns = [
    path("", panel_view, name="panel"),
    path("login-as/<str:username>/", login_as_view, name="login_as"),
    path("reset-db/", reset_db_view, name="reset_db"),
]
