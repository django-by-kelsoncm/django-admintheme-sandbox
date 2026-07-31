from django.urls import path
from .views import PublicFormDemoView, sucesso_view

app_name = "public_forms"

urlpatterns = [
    path("", PublicFormDemoView.as_view(), name="demo"),
    path("sucesso/", sucesso_view, name="sucesso"),
]
