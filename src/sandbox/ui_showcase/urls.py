from django.urls import path
from .views import ShowcaseView

app_name = "ui_showcase"

urlpatterns = [
    path("", ShowcaseView.as_view(), name="showcase"),
]
