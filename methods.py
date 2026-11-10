import cv2
import numpy as np

def linContrStr(img):
    # Calculate min and max pixel values
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab_img)

    min_l = np.min(l_ch)
    max_l = np.max(l_ch)

    if(min_l < max_l):
        l_str = cv2.normalize(l_ch, None,0,255,cv2.NORM_MINMAX)
    else:
        l_str = l_ch

    #restore to bgr 
    str_lab = cv2.merge([l_str,a_ch,b_ch])
    str_bgr = cv2.cvtColor(str_lab, cv2.COLOR_LAB2BGR)

    return str_bgr


def histEq(img):
    # Calculate min and max pixel values
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab_img)

    min_l = np.min(l_ch)
    max_l = np.max(l_ch)

    if(min_l < max_l):
        l_he = cv2.equalizeHist(l_ch)
    else:
        l_he = l_ch

    #restore to bgr 
    he_lab = cv2.merge([l_he,a_ch,b_ch])
    he_bgr = cv2.cvtColor(he_lab, cv2.COLOR_LAB2BGR)

    return he_bgr

def gammaCorr(img):
    ## [changing-contrast-brightness-gamma-correction]
    gamma = 1.25
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv2.LUT(img, lookUpTable)

    return res
