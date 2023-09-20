from django.core.validators import RegexValidator


class RecipeNameValidator(RegexValidator):
    regex = '[a-zA-Zа-яА-ЯёЁ]+'
    message = 'Название должно содержать буквы'
