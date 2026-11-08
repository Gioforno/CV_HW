import cv2
import numpy as np
import pandas as pd

def visualizeCombos(img1, img2, arr_img_ehn, i):
    rescale = 0.3 if (i == 1 or i == 2) else 0.10 #for better visualization, not affect metrics
    ehn_method = ["linear contrast stretching","histogram equalization","linear constrast stretching + gamma correction"]
    ehn_path = ["linear_contrast_stretched_","histogram_equalized_","linear_contrast_stretched_gamma_corrected_"]

    for j in range(0,3):
        name = "visual analysis (original - degradated - enhanced) of photo_" + str(i) + " with " + ehn_method[j]
        
        vis = np.concatenate(
                (    
                cv2.resize(img1, None, fx=rescale, fy=rescale, interpolation=cv2.INTER_AREA),  #original
                cv2.resize(img2, None, fx=rescale, fy=rescale, interpolation=cv2.INTER_AREA),  #degradated
                cv2.resize(arr_img_ehn[j], None, fx=rescale, fy=rescale, interpolation=cv2.INTER_AREA),  #enhanced
                ),
                axis=1)
        
        cv2.imshow(name, vis)
        path = "output/output_img/" + ehn_path[j] + "photo_" + str(i) + ".jpg"
        cv2.imwrite(path, arr_img_ehn[j])
        path2 = "output/output_img/degradated_photo_" + str(i) + ".jpg"
        cv2.imwrite(path2, img2)



    
def saveCsv(PSNR_lcs, PSNR_he, PSNR_g, SSIM_lsc, SSIM_he, SSIM_g):

    names = ['photo_1', 'photo_2', 'photo_3', 'photo_4']
    headers = ['PSNR_lsc', 'PSNR_he', 'PSNR_lcs+g', 'SSIM_lsc', 'SSIM_he', 'SSIM_lcs+g']
    array = np.array([PSNR_lcs, PSNR_he, PSNR_g, SSIM_lsc, SSIM_he, SSIM_g]).T
    
    df = pd.DataFrame(array, columns=headers)
    df.insert(0, 'image', names)   # first column with row labels
    df.to_csv('output/metrics.csv', index=False, float_format='%.4f')