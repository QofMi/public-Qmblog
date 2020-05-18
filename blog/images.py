# Импорт для сжатия иизображения
from io import BytesIO
from PIL import Image
from django.core.files import File

# Импорт для генерирование имени файла
from hashlib import md5
from os import path as op
from time import time

# Сжатиие изображения
def compress(img):
    if img:
        try:
            ext = img.name.split(".")
            if ext[1].lower() == 'jpg':
                im = Image.open(img)
                im_io = BytesIO()
                new = im.resize((1280, 720))
                new.save(im_io, 'JPEG', optimize=True, quality=70)
                new_img = File(im_io, name=img.name)
                return new_img
            elif ext[1].lower() == 'png':
                im = Image.open(img)
                im.convert('P')
                im_io = BytesIO()
                new = im.resize((1280, 720))
                new.save(im_io, 'PNG', optimize=True, quality=70)
                new_img = File(im_io, name=img.name)
                return new_img
        except:
            pass

# Генерирование имени файла

# Для поста
def upload_to(instance, filename, unique=False):
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')
    filename = md5(name.encode('utf8')).hexdigest() + ext
    return op.join('post/', filename)

# Для галерея
def upload_to_gallery(instance, filename, unique=False):
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')
    filename = md5(name.encode('utf8')).hexdigest() + ext
    return op.join('gallery/', filename)
