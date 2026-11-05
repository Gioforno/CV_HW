from matplotlib import pyplot as plt
import cv2
import numpy as np

def visualizeCombos(img1, img2, arr_img_ehn, i):
    rescale = 0.3 if (i == 1 or i == 2) else 0.10 #for better visualization, not affect metrics
    ehn_method = ["linear contrast stretching","histogram equalization","denosing + gamma correction"]

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
        path = "output_img/photo_" + str(i) + " with " + ehn_method[j] +".jpg"
        cv2.imwrite(path, vis)
    
