import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generate_qr_code(unique_code):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(str(unique_code))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), f"{unique_code}.png")