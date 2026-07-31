from django.utils.translation import gettext as _
import datetime
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import (
    display_for_field,
    display_for_value,
    label_for_field,
    lookup_field,
)
from django.contrib.admin.views.main import ORDER_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.template import Library
from django.template.loader import get_template
from django.urls import NoReverseMatch
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.base import InclusionAdminNode

register = Library()


@register.filter
def choices(spec, cl):
    choices_list = list(spec.choices(cl))
    return choices_list


@register.filter
def first_query_param(query_string):
    if not query_string:
        return {}
    for pair in query_string.lstrip("?").split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            return {"name": k, "value": v}
    return {}


def _coerce_field_name(field_name, field_index):
    if callable(field_name):
        if field_name.__name__ == "<lambda>":
            return "lambda" + str(field_index)
        else:
            return field_name.__name__
    return field_name


def result_headers(cl):
    ordering_field_columns = cl.get_ordering_field_columns()
    for i, field_name in enumerate(cl.list_display):
        text, attr = label_for_field(
            field_name, cl.model, model_admin=cl.model_admin, return_attr=True
        )
        is_field_sortable = cl.sortable_by is None or field_name in cl.sortable_by
        if attr:
            field_name = _coerce_field_name(field_name, i)

            if field_name == "action_checkbox":
                aria_label = _("Select all objects on this page for an action")
                yield {
                    "text": mark_safe(
                        f'<input type="checkbox" id="action-toggle" '
                        f'aria-label="{aria_label}">'
                    ),
                    "class_attrib": mark_safe(' class="action-checkbox-column"'),
                    "sortable": False,
                }
                continue

            admin_order_field = getattr(attr, "admin_order_field", None)
            if isinstance(attr, property) and hasattr(attr, "fget"):
                admin_order_field = getattr(attr.fget, "admin_order_field", None)
            if not admin_order_field and LOOKUP_SEP not in field_name:
                is_field_sortable = False

        if not is_field_sortable:
            yield {
                "text": text,
                "class_attrib": format_html(' class="column-{}"', field_name),
                "sortable": False,
            }
            continue

        th_classes = ["sortable", "column-{}".format(field_name)]
        order_type = ""
        new_order_type = "asc"
        sort_priority = 0
        is_sorted = i in ordering_field_columns
        if is_sorted:
            order_type = ordering_field_columns.get(i).lower()
            sort_priority = list(ordering_field_columns).index(i) + 1
            th_classes.append("sorted %sending" % order_type)
            new_order_type = {"asc": "desc", "desc": "asc"}[order_type]

        o_list_primary = []
        o_list_remove = []
        o_list_toggle = []

        def make_qs_param(t, n):
            return ("-" if t == "desc" else "") + str(n)

        for j, ot in ordering_field_columns.items():
            if j == i:
                param = make_qs_param(new_order_type, j)
                o_list_primary.insert(0, param)
                o_list_toggle.append(param)
            else:
                param = make_qs_param(ot, j)
                o_list_primary.append(param)
                o_list_toggle.append(param)
                o_list_remove.append(param)

        if i not in ordering_field_columns:
            o_list_primary.insert(0, make_qs_param(new_order_type, i))

        yield {
            "text": text,
            "sortable": True,
            "sorted": is_sorted,
            "ascending": order_type == "asc",
            "sort_priority": sort_priority,
            "url_primary": cl.get_query_string({ORDER_VAR: ".".join(o_list_primary)}),
            "url_remove": cl.get_query_string({ORDER_VAR: ".".join(o_list_remove)}),
            "url_toggle": cl.get_query_string({ORDER_VAR: ".".join(o_list_toggle)}),
            "class_attrib": (
                format_html(' class="{}"', " ".join(th_classes)) if th_classes else ""
            ),
        }


def items_for_result(cl, result, form):
    def link_in_col(is_first, field_name, cl):
        if cl.list_display_links is None:
            return False
        if is_first and not cl.list_display_links:
            return True
        return field_name in cl.list_display_links

    first = True
    pk = cl.lookup_opts.pk.attname
    for field_index, field_name in enumerate(cl.list_display):
        empty_value_display = cl.model_admin.get_empty_value_display()
        row_classes = ["field-%s" % _coerce_field_name(field_name, field_index)]
        link_to_changelist = link_in_col(first, field_name, cl)
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(
                attr, "empty_value_display", empty_value_display
            )
            if isinstance(value, str) and value.strip() == "":
                value = ""
            if f is None or f.auto_created:
                if field_name == "action_checkbox":
                    row_classes = ["action-checkbox"]
                boolean = getattr(attr, "boolean", False)
                if isinstance(attr, property) and hasattr(attr, "fget"):
                    boolean = getattr(attr.fget, "boolean", False)
                result_repr = display_for_value(value, empty_value_display, boolean)
                if isinstance(value, (datetime.date, datetime.time)):
                    row_classes.append("nowrap")
            else:
                if isinstance(f.remote_field, models.ManyToOneRel):
                    field_val = getattr(result, f.name)
                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        result_repr = field_val
                else:
                    result_repr = display_for_field(
                        value,
                        f,
                        empty_value_display,
                        avoid_link=link_to_changelist,
                    )
                if isinstance(
                    f, (models.DateField, models.TimeField, models.ForeignKey)
                ):
                    row_classes.append("nowrap")
        row_class = mark_safe(' class="%s"' % " ".join(row_classes))
        if link_to_changelist:
            table_tag = "td" if first else "td"
            first = False

            try:
                url = cl.url_for_result(result)
            except NoReverseMatch:
                link_or_text = result_repr
            else:
                url = add_preserved_filters(
                    {"preserved_filters": cl.preserved_filters, "opts": cl.opts}, url
                )
                if cl.to_field:
                    attr = str(cl.to_field)
                else:
                    attr = pk
                value = result.serializable_value(attr)
                link_or_text = format_html(
                    '<a href="{}"{}>{}</a>',
                    url,
                    (
                        format_html(' data-popup-opener="{}"', value)
                        if cl.is_popup
                        else ""
                    ),
                    result_repr,
                )

            yield format_html(
                "<{}{}>{}</{}>", table_tag, row_class, link_or_text, table_tag
            )
        else:
            if (
                form
                and field_name in form.fields
                and not (
                    field_name == cl.model._meta.pk.name
                    and form[cl.model._meta.pk.name].is_hidden
                )
            ):
                bf = form[field_name]
                result_repr = mark_safe(str(bf.errors) + str(bf))
            yield format_html("<td{}>{}</td>", row_class, result_repr)
    if form and not form[cl.model._meta.pk.name].is_hidden:
        yield format_html("<td>{}</td>", form[cl.model._meta.pk.name])


class ResultList(list):
    def __init__(self, form, *items):
        self.form = form
        super().__init__(*items)


def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield ResultList(form, items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            yield ResultList(None, items_for_result(cl, res, None))


def result_hidden_fields(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            if form[cl.model._meta.pk.name].is_hidden:
                yield mark_safe(form[cl.model._meta.pk.name])


def result_list(cl):
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h["sortable"] and h["sorted"]:
            num_sorted_fields += 1
    return {
        "cl": cl,
        "result_hidden_fields": list(result_hidden_fields(cl)),
        "result_headers": headers,
        "num_sorted_fields": num_sorted_fields,
        "results": list(results(cl)),
    }


@register.tag(name="admintheme_sandbox_result_list")

def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser,
        token,
        func=result_list,
        template_name="change_list_results.html",
        takes_context=False,
    )


@register.tag(name="dsgovbr_result_list")
def dsgovbr_result_list_tag(parser, token):
    return result_list_tag(parser, token)


@register.simple_tag
def admintheme_sandbox_admin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    return tpl.render(
        {
            "title": spec.title,
            "choices": list(spec.choices(cl)),
            "spec": spec,
        }
    )


@register.simple_tag
def dsgovbr_admin_list_filter(cl, spec):
    return admintheme_sandbox_admin_list_filter(cl, spec)
