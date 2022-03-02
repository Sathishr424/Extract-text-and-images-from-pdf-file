import pdfplumber, os, sys, json, random, string
from os import path

def randomName():
    return str(''.join(random.choices(string.ascii_uppercase + string.digits, k=12))) + ".png"

# try:
#     if (sys.argv[1]): pdf = sys.argv[1]
#     else: pdf = "../test_pdf.pdf"
# except:
#     pdf = "../test_pdf.pdf"

pdf = sys.argv[1]

print(pdf)
try:
    with open(os.path.join(os.getcwd(), "src", "imageJson"), 'w', encoding='utf-8') as file:
        pdf_obj = pdfplumber.open(path.join(pdf))
        pages = pdf_obj.pages
        ret = []
        for p in range(len(pages)):
            page = pages[p]
            images_in_page = page.images
            page_height = page.height
            #print('Page height:', page_height)
            for image in images_in_page:
                # print(image)
                image_bbox = (image['x0'], page_height - image['y1'], image['x1'], page_height - image['y0'])
                print(image_bbox)
                cropped_page = page.crop(image_bbox)
                image_obj = cropped_page.to_image(resolution=100)
                fPath = os.path.join(os.getcwd(), 'Images', randomName())
                print(fPath)
                image_obj.save(fPath)
                data = {'name': fPath, 'page': p+1, 'x':image['x0'], 'y': image['y0'], 'width': image['width'], 'height': image['height']}
                ret.append(data)
        file.write(json.dumps(ret))
except Exception as e:
    print(e)

print("Convertion finished");
