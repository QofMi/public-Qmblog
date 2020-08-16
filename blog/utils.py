from django.utils.text import slugify
from time import time

# Алфавит для перевода из кириллицы в транслит
alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def _gen_slug(slug):
    """
    Генерация slug и перевод из кириллицы в транслит
    """
    new_slug = slugify(''.join(alphabet.get(w, w) for w in slug.lower()))
    return new_slug + '-' + str(int(time()))
