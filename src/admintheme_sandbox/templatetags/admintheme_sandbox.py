from django import template
from django.utils.safestring import SafeString, mark_safe
from django.contrib.admin.views.main import PAGE_VAR

register = template.Library()


@register.filter
def first_word(value: str) -> str:
    return str(value).split(" ")[0]


@register.filter
def last_word(value: str) -> str:
    return str(value).split(" ")[0]


@register.filter
def user_letters(user):
    return user.first_name[:1].upper()


@register.simple_tag
def page_item(cl, page) -> SafeString:
    if page == cl.paginator.ELLIPSIS:
        extra_class = "disabled"
    elif page == cl.page_num:
        extra_class = "active"
    else:
        extra_class = ""

    url = cl.get_query_string({PAGE_VAR: page})

    return mark_safe(
        f"""<li class="paginate_button page-item {extra_class}"><a href="{url}"
            data-dt-idx="{page}" tabindex="{page}" class="page-link">{page}</a></li>"""
    )
