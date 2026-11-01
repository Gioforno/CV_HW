import cv2
import numpy as np
from tabulate import tabulate

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

def fillTable(value_od, value_de, value_oe):
    data = [[],[],[],[]]
    for i in range(0,4):
        data[i] = ["image " + str(i+1),value_od[i], value_de[i],value_oe[i]]
    headers = ["image","od","de","oe"]
    table = tabulate(data, headers, tablefmt="grid")
    return table



#default init
PSNR_value_od = [0,0,0,0]
PSNR_value_de = [0,0,0,0]
PSNR_value_oe = [0,0,0,0]
SSIM_value_od = [0,0,0,0]
SSIM_value_de = [0,0,0,0]
SSIM_value_oe = [0,0,0,0]

#INITIAL DEGRADATION
for i in range (1,5):
    path = "original_images/photo_" + str(i) + ".jpg"
    o_img = cv2.resize(cv2.imread(path), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) 

    new_img = degradate(o_img)

    PSNR_value_od[i-1] = round(cv2.PSNR(o_img, new_img),2)

    name = str(i) + " - combo (sx original, dx degradated)" 
    vis = np.concatenate((o_img, new_img), axis=1)
    cv2.imshow(name, vis)




#TABLE CONSTRUCTORS
PSNRTable = fillTable(PSNR_value_od, PSNR_value_de, PSNR_value_oe)

print("\n\nPSNR TABLE\nod: original-degradated, de: degradated-enhanced, oe: original-enhanced")
print(PSNRTable)

SSIMTable = fillTable(SSIM_value_od, SSIM_value_de, SSIM_value_oe)











cv2.waitKey(0) #wait for any key to close windows
cv2.destroyAllWindows() #destroy all the windows at the end of the program for have a safe memory
