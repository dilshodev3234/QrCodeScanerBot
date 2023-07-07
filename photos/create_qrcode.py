import os
from multiprocessing.pool import Pool

import qrcode
from fpdf import FPDF

from db.model import Qrcodes

pdf = FPDF()


def t(i):
    data = f"https://t.me/BOONVI_bot?start={i}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image()
    qr_filename = f'{i}.png'
    qr_image.save(qr_filename)
    pdf.add_page()
    pdf.image(qr_filename, x=10, y=10, w=190)
    Qrcodes().insert_into(id=i, active=False)
    os.remove(qr_filename)

with Pool() as p:
    p.map(t, range(1, 10051))


pdf.output("qrcodes.pdf", "F")
