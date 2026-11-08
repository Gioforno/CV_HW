import cv2
from skimage.metrics import structural_similarity as compare_ssim

def SSIMcalc(o_img, d_img):

    # Convert to grayscale
    o_grayscale = cv2.cvtColor(o_img, cv2.COLOR_BGR2GRAY)
    d_grayscale = cv2.cvtColor(d_img, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    (score, diff) = compare_ssim(o_grayscale, d_grayscale, full=True)

    return score
