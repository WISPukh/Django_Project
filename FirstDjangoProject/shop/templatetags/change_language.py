from django import template

register = template.Library()


@register.simple_tag
def change_language(request, lang_code):
    if request.path.startswith(f'/{lang_code}'):
        return request.path
    return f'/{lang_code + request.path[3:]}'
