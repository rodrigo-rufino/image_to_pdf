# This script merges a set of images into a pdf file cointaining all of them.

from PIL import Image
import os
from pyPdf import PdfFileReader, PdfFileWriter


def image_to_pdf(filename):
    if filename.endswith(".png") or \
        filename.endswith(".jpg"):

        if "png" in filename:
            new_filename = filename.replace("png", "pdf")
        if "jpg" in filename:
            new_filename = filename.replace("jpg", "pdf")

        # Convert image to RGB
        im = Image.open(filename)
        if (im.mode == "RGBA"):
            im = im.convert("RGB")

        # Create pdf file
        if not os.path.exists(new_filename):
            im.save(new_filename, "PDF", resolution=100.0)


def dir_images_to_pdf(directory):
    for filename in os.listdir(directory):
        image_to_pdf(filename)


def merge_pdfs(directory):
    output = PdfFileWriter()
    output_file = "output.pdf"
    open_pdfs = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            f = open(filename, "rb")
            pdf = PdfFileReader(f)
            output.addPage(pdf.getPage(0))
            open_pdfs.append(f)
            
    if not os.path.isfile(output_file):
        outputStream = file(output_file, "wb")
        output.write(outputStream)
    else:
        print "The file \"" + output_file + "\" already exists."

    # Close all open pdfs. They need to be closed here because outputStream still
    # uses them.
    for f in open_pdfs:
        f.close()

    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and not filename==output_file:
            os.remove(filename)


if __name__=="__main__":
    directory = "./"
    image_to_pdf(directory)
    merge_pdfs(directory)