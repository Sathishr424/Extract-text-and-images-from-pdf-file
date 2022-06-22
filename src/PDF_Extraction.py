import fitz, json
from pdfminer import layout
from pdfminer.high_level import extract_pages
from os import path
import os
import sys

data = {"image":[], "text":[]}

# print(os.getcwd())

def getObject(object, page):
    global data
    #print(object)
    if isinstance(object, layout.LTText):
        if not isinstance(object, layout.LTTextLine):
            for child in object:
                getObject(child, page)
        else:
            if len(object.get_text().strip()) > 0:
                cord = object.bbox
                data['text'].append({'str':object.get_text().strip(), 'page': page, 'x': cord[0], 'y':cord[1], 'width': object.width, 'height': object.height})
    elif isinstance(object, layout.LTImage):
        ePath = path.join(os.getcwd(), "Images", str(os.path.splitext(object.name)[0]) + ".png")
        cord = object.bbox
        data['image'].append({'name':object.name, 'path': ePath, 'page': page, 'x': cord[0], 'y':cord[1], 'width': object.width, 'height': object.height})
    elif isinstance(object, layout.LTContainer):
        for child in object:
            getObject(child, page)

def main(pdf):
    pdf_path = os.path.join(pdf)

    try:
        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            # with open('test'+str(i+1)+'.json', 'w') as file: file.write(json.dumps(doc[i].get_text("json")))
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                try:
                    if pix.n < 5:       # this is GRAY or RGB
                        pix.writePNG(os.path.join(os.getcwd(), "Images", "%s.png" % (img[-2])))
                    else:               # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.writePNG(os.path.join(os.getcwd(), "Images", "%s.png" % (img[-2])))
                        pix1 = None
                except:
                    pass
                pix = None
    except:
        print("Error extracting image!")

    try:
        pages = list(extract_pages(pdf_path))

        for p in range(len(pages)):
            getObject(pages[p], p+1)

        with open(os.path.join(os.getcwd(), 'jsonData.json'), 'w') as file:
            file.write(json.dumps(data, indent=2))
    except:
        print("Error extracting text!")

    #print(data)

if __name__ == "__main__":
    main('16.pdf')
    #if (len(sys.argv) > 1):
        #main(sys.argv[1])
    #else:
        #print("Please pass an argument!")