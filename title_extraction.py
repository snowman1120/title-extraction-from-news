import cv2
import pytesseract
from pytesseract import Output

def getting_textdata(img, conf, zoom_fac, split_val):
    '''
    img: soucr image to process.
    conf: tesseract conf (--psm xx)
    zoom_fac: image resize factor.
    split_val: factor to consider for coordinate of texts when image is splited into two parts
    '''
    d = pytesseract.image_to_data(img, output_type=Output.DICT, config=conf)
    text_ori = d['text']
    left_coor, top_coor, wid, hei, conf = d['left'], d['top'], d['width'], d['height'], d['conf']        
    ### removing None element from text ###
    text, left, top, w, h, accu, xc, yc= [], [], [], [], [], [], [], []
    for cnt, te in enumerate(text_ori):
        if te.strip() != '' and wid[cnt] > 10 and hei[cnt] > 10:
            text.append(te)
            left.append(int((left_coor[cnt]+split_val)/zoom_fac))
            top.append(int(top_coor[cnt]/zoom_fac))
            w.append(int(wid[cnt]/zoom_fac))
            h.append(int(hei[cnt]/zoom_fac))
            accu.append(conf[cnt])    
            xc.append(int((left_coor[cnt]+wid[cnt]/2+split_val)/zoom_fac))
            yc.append(int((top_coor[cnt]+hei[cnt]/2)/zoom_fac))
    return text, left, top, w, h, accu, xc, yc
img = cv2.imread("inputs/01_04_2016_001_010.jpg")
text, left, top, w, h, accu, xc, yc = getting_textdata(img, 'psm --6', 1, 0)
for i in range(len(text)):
    img = cv2.rectangle(img, (left[i], top[i]), (left[i]+w[i], top[i]+h[i]), (0, 0, 255), 3) 
cv2.imwrite('img.jpg', img)