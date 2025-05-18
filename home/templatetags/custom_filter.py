from django import template
register = template.Library()
import calendar


@register.filter
def get_item(dictionary, key):
    try:
        if dictionary is not None and key is not None:
            return dictionary.get(key)
    except AttributeError:
        pass
    return None

ARABIC_MONTHS = {
    1: "يناير",
    2: "فبراير",
    3: "مارس",
    4: "أبريل",
    5: "ماي",
    6: "يونيو",
    7: "يوليوز",
    8: "غشت",
    9: "شتنبر",
    10: "أكتوبر",
    11: "نونبر",
    12: "دجنبر",
}

@register.filter
def get_month(number):
    return ARABIC_MONTHS.get(number)