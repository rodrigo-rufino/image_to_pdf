# This script merges a set of images into a pdf file cointaining all of them.

from PIL import Image
import os
import sys
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
    elif filename.endswith(".pdf"):
        pass
    else:
        print "No Images found to convert."


def dir_images_to_pdf(directory):
    for filename in os.listdir(directory):
        filename = directory + "\\" + filename
        image_to_pdf(os.path.abspath(filename))
        print "Converting: ", filename


def merge_pdfs(directory):
    output = PdfFileWriter()

    # name of the output file is the same as the folder
    output_file = directory + "\\" + directory.split("\\")[-1] + ".pdf"
    return_output = output_file

    open_pdfs = []
    contains_pdf = False

    for filename in os.listdir(directory):
        # full filename is directory path + filename
        filename = directory + "\\" + filename
        if filename.endswith('.pdf') and not filename==output_file:
            contains_pdf = True
            break    
        else:
            print "No PDFs found to merge at " + filename
            break

    if not os.path.isfile(output_file) and contains_pdf:
        for filename in os.listdir(directory):
            filename = directory + "\\" + filename
            if filename.endswith(".pdf"):
                f = open(filename, "rb")
                pdf = PdfFileReader(f)
                output.addPage(pdf.getPage(0))
                open_pdfs.append(f)
        outputStream = file(output_file, "wb")
        output.write(outputStream)

    elif os.path.isfile(output_file):
        print "The file \"" + output_file + "\" already exists."
    # If the file don't exist and it wasn't possible to create it
    else:
        return_output = ""

    # Close all open pdfs. They need to be closed here because outputStream still
    # uses them.
    for f in open_pdfs:
        f.close()

    for filename in os.listdir(directory):
        filename = directory + "\\" + filename
        if filename.endswith(".pdf") and not filename==output_file:
            print "Removing: ", filename
            os.remove(filename)

    print "PDF saved at " + return_output + "\n"
    return return_output


def move_all_to_output(files):

    destiny_folder =  os.getcwd() + "\\output\\"

    if not os.path.exists(destiny_folder):
        os.mkdir(destiny_folder)

    for f in files:
        try:
            if f:
                destiny_file =  os.getcwd() + "\\output\\" + f.split("\\")[-1]
                os.rename(f, destiny_file)
        except Exception as e:
            print e
    
    print "\nFiles saved at: " + destiny_folder

        


if __name__=="__main__":
    
    # Current directory
    if len(sys.argv) == 1:
        directory = "./"
        dir_images_to_pdf(directory)
        merge_pdfs(directory)
    # For multiple directories
    else:
        files = []
        for arg in sys.argv[1:]:
            if os.path.isdir(arg) and not arg=="output":
                directory = os.path.abspath(arg)

                dir_images_to_pdf(directory)

                files.append(merge_pdfs(directory))

        move_all_to_output(files)

    # For multiple subdirectories (uncomment the bellow section)