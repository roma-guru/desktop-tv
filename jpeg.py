import io
from PIL import Image


def to_jpeg(pic, size):
    i = Image.frombytes("RGB", size, pic)
    buf = io.BytesIO()
    i.save(buf, format="jpeg")
    buf.seek(0)
    jpeg_data = buf.read()
    return jpeg_data
