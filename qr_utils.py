import qrcode
from PIL import Image
import numpy as np
import cv2
import io

def generate_qr(text):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(text)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def pil_to_bytes(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()

def decode_qr(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data if data else None
