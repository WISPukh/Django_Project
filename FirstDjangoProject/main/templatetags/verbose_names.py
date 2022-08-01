from django import template

register = template.Library()


@register.filter
def get_verbose_field_name(instance):
    exclude_field = (
        'content_type',
        'product_ptr',
        'id'
    )
    for name in instance._meta.fields:
        if name.name not in exclude_field:
            yield name.verbose_name, name.value_to_string(instance)
