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
    im = Image.open(img)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', optimize=True, quality=70)
    new_img = File(im_io, name=img.name)
    return new_img

# Генерирование имени файла
def upload_to(instance, filename, unique=False):
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')
    filename = md5(name.encode('utf8')).hexdigest() + ext
    return op.join('img/', filename)
