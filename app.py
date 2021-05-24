from datetime import datetime

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.platypus import Frame
from reportlab.lib import utils
from PIL import Image
from urllib.request import urlopen
from io import BytesIO

from testdata import asset_info

def get_project_creation_time():
    current_dt = datetime.now()
    current_dt_string = current_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    return current_dt_string

def get_image(path, width=1*cm):
    im = Image.open(urlopen(path))
    iw, ih = im.size
    aspect = ih / float(iw)
    height=(width * aspect)
    return im.resize((int(width), int(height)), Image.ANTIALIAS)


def generate_report():
    creation_time = get_project_creation_time()
    canvas = Canvas("hello.pdf", pagesize=A4)
    canvas.setFont("Helvetica", 12)
    print()
    canvas.drawString(A4[0]-inch, A4[1]-inch, "Hello, World")
    canvas.drawImage("https://hub.hammermissions.com/assets/logo.png", A4[0]-inch, A4[1]-3*inch, 70, 70, preserveAspectRatio=True)
    canvas.drawString(72, 72, f"Created: {creation_time}")
    # canvas.drawImage("hammer-logo.png", 100, 100, 200, 200, preserveAspectRatio=True)
    # TODO-DEREK 1. Summary page - map; all thumbnails. (use Platypus)
    # TODO-DEREK 1. Figure out overall layout. (use Platypus)
    # TODO-DEREK 2. Get annotations to appear.
    for asset in asset_info["data"]:
        canvas.showPage()
        image = get_image(asset["url"], width=600)
        im_data = BytesIO()
        image.save(im_data, format='png')
        im_data.seek(0)
        img_out = utils.ImageReader(im_data)
        iw, ih = image.size
        canvas.drawImage(img_out, 100, 100, iw, ih, preserveAspectRatio=True)
    canvas.save()

if __name__ == "__main__":
    project_info = {
        "name": "ASDA - Basingstoke Roof Condition",

    }
    # print(asset_info)
    generate_report()
