from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Возвращает значение словаря по указанному ключу."""
    if isinstance(dictionary, dict):  # Проверяем, что передан именно словарь
        return dictionary.get(key, [])
    return []