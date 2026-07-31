from django.views.generic import TemplateView


class ShowcaseView(TemplateView):
    template_name = "ui_showcase/showcase.html"
