import cv2
import numpy as np
from tabulate import tabulate
from skimage.metrics import structural_similarity as compare_ssim

#TODO
# degradate original image OK
#
# enhancement respect to degradated (same param for all photo --> single function) 
#   original photo
#   linear contrast stretiching
#   histogram equalization
#   gamma correction/simplified homomorphic filter/classical denoising/combo of methods
#
# evaluation parameters
#   PSNR in respect to original OK
#   SSIM or manually implemented (for example, mean absolute error or mean squared error)
#
# compare different methods on at least two images
#
# table of comparison
#   fix representation OK
#
# docs


def degradate(img):
    alpha = 0.5 # [1.0;3.0]
    beta = 20 # [0;100]
    mean = 0
    stddev = 180
    noise = np.zeros(o_img.shape, np.uint8)
    cv2.randn(noise, mean, stddev)
    noisy_img = cv2.add(o_img, noise)
    new_img = cv2.convertScaleAbs(noisy_img, alpha=alpha, beta=beta)
    
    return new_img

def fillTable(value_o, value_lsc, value_he, value_lsc_he):
    data = [[],[],[],[]]
    for i in range(0,4):
        data[i] = ["image " + str(i+1),value_o[i], value_lsc[i],value_he[i] ,value_lsc_he[i]]
    headers = ["degradated image","original","linear contrast stretching","histogram equalization", "linear contrast stretching + histogram equalization"]
    table = tabulate(data, headers, tablefmt="grid")
    return table

def SSIMcalc(o_img, d_img):

    # Convert to grayscale
    o_grayscale = cv2.cvtColor(o_img, cv2.COLOR_BGR2GRAY)
    d_grayscale = cv2.cvtColor(d_img, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    (score, diff) = compare_ssim(o_grayscale, d_grayscale, full=True)

    return score

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
    

#default init
# all data referred to degradated image vs
#                                           o: original
#                                           lsc: linear contrast stretching


PSNR_o = [0,0,0,0]
SSIM_o = [0,0,0,0]
PSNR_lsc = [0,0,0,0]
SSIM_lsc = [0,0,0,0]
PSNR_he = [0,0,0,0]
SSIM_he = [0,0,0,0]
PSNR_lsc_he = [0,0,0,0]
SSIM_lsc_he = [0,0,0,0]

#CYCLE ON 4 IMAGE
for i in range (1,5):

    #load img and rescale to standard size
    path = "original_images/images/photo_" + str(i) + ".jpg"
    o_img = cv2.resize(cv2.imread(path), None, fx=0.15, fy=0.15, interpolation=cv2.INTER_AREA) 

#DEGRADATION
    #degradate img reduncing contrast and adding gaussian noise
    d_img = degradate(o_img)

    #compute PSNR and SSIM of degradated image
    PSNR_o[i-1] = round(cv2.PSNR(o_img, d_img),2)
    SSIM_o[i-1] = SSIMcalc(o_img, d_img)

#LINEAR CONTRAST STRETCHING (only of d_img as requested)
    lsc_img = linContrStr(o_img) 
    PSNR_lsc[i-1] = round(cv2.PSNR(d_img, lsc_img),2)
    SSIM_lsc[i-1] = SSIMcalc(d_img, lsc_img)


#HISTOGRAM EQUALIZATION
    he_img = histEq(o_img)
    PSNR_he[i-1] = round(cv2.PSNR(d_img, he_img),2)
    SSIM_he[i-1] = SSIMcalc(d_img, he_img)

    lsc_he_img = linContrStr(histEq(o_img))
    PSNR_lsc_he[i-1] = round(cv2.PSNR(d_img, lsc_he_img),2)
    SSIM_lsc_he[i-1] = SSIMcalc(d_img, lsc_he_img)

    #concatenate in the same visualization original image, degradated image and enhanced image
    name = str(i) + " - combo (sx original, cx degradated, dx lcs)" 
    vis = np.concatenate((d_img, o_img, lsc_img, he_img, lsc_he_img), axis=1)
    cv2.imshow(name, vis)




#TABLE CONSTRUCTORS
PSNRTable = fillTable(PSNR_o, PSNR_lsc, PSNR_he, PSNR_lsc_he)

print("\n\nPSNR TABLE")
print(PSNRTable)


print("\n\nSSIM TABLE: 1 high similarity, 0 no similarity, negative means two different images")
SSIMTable = fillTable(SSIM_o, SSIM_lsc, SSIM_he, SSIM_lsc_he)
print(SSIMTable)




cv2.waitKey(0) #wait for any key to close windows
cv2.destroyAllWindows() #destroy all the windows at the end of the program for have a safe memory
