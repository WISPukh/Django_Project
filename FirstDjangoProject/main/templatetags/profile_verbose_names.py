from django import template

register = template.Library()


@register.filter
def get_verbose_profile_name(instance):
    exclude_field = (
        'id',
        'user'
    )
    for name in instance._meta.fields:
        if name.name not in exclude_field:
            yield name.verbose_name, name.value_to_string(instance)
