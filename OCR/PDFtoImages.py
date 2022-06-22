import fitz, json
import os, shutil, sys
from PIL import Image

# Libraries needed
# pymupdf, pillow

if not os.path.isdir(os.path.join(os.getcwd(), "Pages")):
    os.mkdir(os.path.join(os.getcwd(), "Pages"))
if not os.path.isdir(os.path.join(os.getcwd(), "Converted")):
    os.mkdir(os.path.join(os.getcwd(), "Converted"))

def deleteFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def main(pdf):
    try:
        deleteFolder(os.path.join(os.getcwd(), 'Pages'))
    except:
        pass
    
    pdffile = pdf
    doc = fitz.open(pdffile)
    
    for i in range(len(doc)):
        page = doc.loadPage(i)
        pix = page.get_pixmap()
        output = os.path.join(os.getcwd(), 'Pages', str(i+1) + ".png")
        #print(output)
        pix.save(output)
    
    images = []
    images_path = os.listdir(os.path.join(os.getcwd(), "Pages"))
    for i in range(len(images_path)):
        images_path[i] = int(images_path[i][:-4])
    images_path.sort()
    for i in range(len(images_path)):
        images_path[i] = str(images_path[i]) + ".png"
    #images_path.sort()
    for i in images_path: print(i)
    for i in images_path:
        images.append(Image.open(os.path.join(os.getcwd(), "Pages", i)))
    
    pdf_path = os.path.join(os.getcwd(), 'Converted', 'Pdf.pdf')
    
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
    print("Script ends..")

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        main(sys.argv[1])
    else:
        print("Please pass an argument!")