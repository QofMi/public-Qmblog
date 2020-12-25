# Импорт для сжатия иизображения
from io import BytesIO
from PIL import Image
from django.core.files import File

# Импорт для генерирования имени файла
from hashlib import md5
from os import path as op
from time import time


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


def upload_to(instance, filename, unique=False):
    """
    Генерирование имени файла для изображений можели Post
    """
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')
    filename = md5(name.encode('utf8')).hexdigest() + ext
    return op.join('post/', filename)


def upload_to_gallery(instance, filename, unique=False):
    """
    Генерирование имени файла для изображений можели Gallery
    """
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')
    filename = md5(name.encode('utf8')).hexdigest() + ext
    return op.join('gallery/', filename)
