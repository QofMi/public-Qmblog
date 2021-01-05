# Импорт для сжатия иизображения
from io import BytesIO
from PIL import Image
from django.core.files import File

# Импорт для генерирования имени файла
import os
from time import time
from hashlib import md5
from django.utils.deconstruct import deconstructible


def _compressing_image(img):
    """
    Сжатиие изображения
    """
    im = Image.open(img)
    im_io = BytesIO()
    new = im.resize((1280, 720))
    new = im.convert('RGB')
    new.save(im_io, 'JPEG', optimize=True, quality=70)
    new_img = File(im_io, name=img.name)
    return new_img


@deconstructible
class GenFilename(object):
    """
    Генерирование имени файла при его загрузке
    """
    def __init__(self, path):
        self.path = os.path.join(path, '%s%s')

    def __call__(self, instance, filename, unique=False):
        extension = os.path.splitext(filename)[1]
        name = str(instance.pk or '') + filename + (str(time()) if unique else '')
        filename = md5(name.encode('utf8')).hexdigest()
        return self.path % (filename, extension)
