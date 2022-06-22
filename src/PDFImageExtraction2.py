from select import epoll
from pdfminer import layout
from pdfminer.high_level import extract_pages
from PIL import Image
from os import path
import os
from pdfminer.image import ImageWriter
import io, json

print(os.getcwd())
data = {"image":[], "text":[]}

def getObject(object, page):
    if isinstance(object, layout.LTText):
        if not isinstance(object, layout.LTTextLine):
            for child in object:
                getObject(child, page)
        else:
            if len(object.get_text().strip()) > 0:
                cord = object.bbox
                data['text'].append({'str':object.get_text().strip(), 'page': page, 'x': cord[0], 'y':cord[1], 'width': object.width, 'height': object.height})
    elif isinstance(object, layout.LTImage):
        ePath = path.join(os.getcwd(), "Images")
        cord = object.bbox
        data['image'].append({'name':object.name, 'path': path.join(ePath, object.name), 'page': page, 'x': cord[0], 'y':cord[1], 'width': object.width, 'height': object.height})
    elif isinstance(object, layout.LTContainer):
        for child in object:
            getObject(child, page)

pdf_path = path.join('/home/sathish/Documents/Personal Projects/Extract text and images from pdf file/src/Sample Market Research.pdf')

pages = list(extract_pages(pdf_path))

for p in range(len(pages)):
    getObject(pages[p], p+1)

with open(path.join('/home/sathish/Documents/Personal Projects/Extract text and images from pdf file/src', 'jsonData.json'), 'w') as file:
    file.write(json.dumps(data, indent=2))
print(json.dumps(data['image'], indent=2))
