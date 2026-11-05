import cv2
import numpy as np
from table import *
from visualize import visualizeCombos
from metrics import *


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



#default init
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

#LINEAR CONTRAST STRETCHING
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
    print("\n\n\n\n\n\n\n METRICS TABLE OF photo_" +str(i))
    print(PSNRTableSing)


    print("\n\nPress any key to analyze next image")
    cv2.waitKey(0) #wait for any key to close windows
    cv2.destroyAllWindows() #destroy all the windows at the end of the program for have a safe memory


#SUMMARY TABLE
print("\n\n\n\n\n\nSummary table with metrics")

PSNRTable = fillTable(PSNR_lsc, PSNR_he, PSNR_g)
print("\nPSNR TABLE")
print(PSNRTable)


print("\n\nSSIM TABLE: 1 high similarity, 0 no similarity, negative means two different images")
SSIMTable = fillTable(SSIM_lsc, SSIM_he, SSIM_g)
print(SSIMTable)


print("All images seen during the execution are inside the folder output_img/")
