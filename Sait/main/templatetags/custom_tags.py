from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Возвращает значение словаря по указанному ключу."""
    return dictionary.get(key, [])
