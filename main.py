import cv2
import numpy as np
from tabulate import tabulate
from skimage.metrics import structural_similarity as compare_ssim

#TODO
# choose only 4 img (more particular for each case)
# degradate original image OK
#
# enhancement respect to degradated (same param for all photo --> single function)  OK
#   original photo OK
#   linear contrast stretiching OK
#   histogram equalization OK
#   gamma correction + classical denoising OK
#
# evaluation parameters
#   PSNR in respect to original OK
#   SSIM or manually implemented (for example, mean absolute error or mean squared error) OK
#
# compare different methods on at least two images OK
#
# table of comparison
#   fix representation OK
# 
# representation: 
#   if have time, represent better with mathplotlib instead cv2.imshow

# docs


def degradate(img):
    alpha = 0.7
    beta = 30
    mean = 0
    stddev = 50 
    noise = np.zeros(img.shape, np.uint8)
    cv2.randn(noise, mean, stddev)
    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    noisy_img = cv2.add(new_img, noise)
    
    return noisy_img

def fillTable(value_lsc, value_he, value_g):
    data = [[],[],[],[]]
    for i in range(0,4):
        data[i] = ["photo_" + str(i), value_lsc[i],value_he[i] ,value_g[i]]
    headers = ["original image","linear contrast stretching","histogram equalization", "denoising + gamma correction"]
    table = tabulate(data, headers, tablefmt="grid")
    return table

def fillTableSing(PSNR_lsc, PSNR_he, PSNR_g,SSIM_lsc, SSIM_he, SSIM_g,i):
    data = [
        ["PSNR", PSNR_lsc,PSNR_he,PSNR_g],
        ["SSIM", SSIM_lsc,SSIM_he,SSIM_g]
        ]
    headers = ["METRICS","linear contrast stretching","histogram equalization", "denoising + gamma correction"]
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

def gammaCorr(img):
    ## [changing-contrast-brightness-gamma-correction]
    gamma = 0.25
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv2.LUT(img, lookUpTable)

    return res

def visualizeCombos(img1, img2, arr_img_ehn, i):
    rescale = 0.4 if (i == 1 or i == 2) else 0.14 #for better visualization, not affect metrics
    ehn_method = ["linear contrast stretching","histogram equalization","denosing + gamma correction"]

    for j in range(0,3):
        name = "visual analysis of photo_" + str(i) + " with " + ehn_method[j] + " method"
        vis = np.concatenate(
                (    
                cv2.resize(img1, None, fx=rescale, fy=rescale, interpolation=cv2.INTER_AREA),  #original
                cv2.resize(img2, None, fx=rescale, fy=rescale, interpolation=cv2.INTER_AREA),  #degradated
                cv2.resize(arr_img_ehn[j], None, fx=rescale, fy=rescale, interpolation=cv2.INTER_AREA),  #enhanced
                ),
                axis=1)
        
        cv2.imshow(name, vis)
    
    


#default init
# all data referred to degradated image vs
#                                           o: original
#                                           lsc: linear contrast stretching


PSNR_do = [0,0,0,0]
SSIM_do = [0,0,0,0]

PSNR_lsc = [0,0,0,0]
SSIM_lsc = [0,0,0,0]
PSNR_he = [0,0,0,0]
SSIM_he = [0,0,0,0]
PSNR_g = [0,0,0,0]
SSIM_g = [0,0,0,0]


#CYCLE ON 4 IMAGE
for i in range (1,5):

    #load img and rescale to standard size
    path = "original_images/photo_" + str(i) + ".jpg"
    o_img = cv2.imread(path)

#DEGRADATION
    #degradate img reduncing contrast and adding gaussian noise
    d_img = degradate(o_img)

    #compute PSNR and SSIM of degradated image
    PSNR_do[i-1] = cv2.PSNR(o_img, d_img)
    SSIM_do[i-1] = SSIMcalc(o_img, d_img)


#LINEAR CONTRAST STRETCHING (only of d_img as requested)
    lsc_img = linContrStr(d_img) 
    PSNR_lsc[i-1] = cv2.PSNR(o_img, lsc_img)
    SSIM_lsc[i-1] = SSIMcalc(o_img, lsc_img)


#HISTOGRAM EQUALIZATION
    he_img = histEq(d_img)
    PSNR_he[i-1] = cv2.PSNR(o_img, he_img)
    SSIM_he[i-1] = SSIMcalc(o_img, he_img)



#DENOISING + GAMMA CORRECTION
    g_img =(linContrStr(gammaCorr(d_img)))
    PSNR_g[i-1] = cv2.PSNR(o_img, g_img)
    SSIM_g[i-1] = SSIMcalc(o_img, g_img)


#VISUALIZATION
    ehn_img = [lsc_img,he_img,g_img]
    visualizeCombos(o_img,d_img,ehn_img,i)

    PSNRTableSing = fillTableSing(PSNR_lsc[i-1], PSNR_he[i-1], PSNR_g[i-1],SSIM_lsc[i-1], SSIM_he[i-1], SSIM_g[i-1],i)
    print("\n\n METRICS TABLE OF photo_" +str(i))
    print(PSNRTableSing)


    print("\n\nPress any key to analyze next image")
    cv2.waitKey(0) #wait for any key to close windows
    cv2.destroyAllWindows() #destroy all the windows at the end of the program for have a safe memory


#TABLE CONSTRUCTORS

print("\n\nSummary table with metrics")

PSNRTable = fillTable(PSNR_lsc, PSNR_he, PSNR_g)
print("\n\nPSNR TABLE")
print(PSNRTable)



print("\n\nSSIM TABLE: 1 high similarity, 0 no similarity, negative means two different images")
SSIMTable = fillTable(SSIM_lsc, SSIM_he, SSIM_g)
print(SSIMTable)

