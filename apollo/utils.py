# -*- coding: utf-8 -*-
import codecs
import os
import warnings
from datetime import datetime, timezone
from uuid import UUID, uuid4

from PIL import Image
from pytz import utc


def read_env(env_path=None):
    if not os.path.exists(env_path):
        warnings.warn('No environment file found. Skipping load.')
        return

    for k, v in parse_env(env_path):
        os.environ.setdefault(k, v)


def parse_env(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.strip('"').strip("'")
            yield k, v


def current_timestamp() -> datetime:
    return datetime.now(tz=timezone.utc)


def naive_current_timestamp() -> datetime:
    return current_timestamp().replace(tzinfo=None)


def validate_uuid(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False


def remove_bom_in_place(path):
    buffer_size = 4096
    bom_length = len(codecs.BOM_UTF8)

    with open(path, 'r+b') as fp:
        chunk = fp.read(buffer_size)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[bom_length:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(bom_length, os.SEEK_CUR)
                chunk = fp.read(buffer_size)
            fp.seek(-bom_length, os.SEEK_CUR)
            fp.truncate()


def strip_bom_header(fileobj):
    chunk_size = 512
    chunk = fileobj.read(chunk_size)

    if chunk.startswith(codecs.BOM_UTF8):
        fileobj.seek(len(codecs.BOM_UTF8))
    else:
        fileobj.seek(0)

    return fileobj


def generate_identifier():
    val = int(uuid4()) % 100000000000000
    return hex(val)[2:-1]


def resize_image(pil_image: Image, new_size: int) -> Image:
    background_color = (255, 255, 255, 0)
    image_mode = 'RGBA'

    width, height = pil_image.size
    if width == height:
        return pil_image.resize((new_size, new_size), Image.LANCZOS)

    if width > height:
        result = Image.new(image_mode, (width, width), background_color)
        result.paste(pil_image, (0, (width - height) // 2))
        return result.resize((new_size, new_size), Image.LANCZOS)
    else:
        result = Image.new(image_mode, (height, height), background_color)
        result.paste(pil_image, ((height - width) // 2, 0))
        return result.resize((new_size, new_size), Image.LANCZOS)
