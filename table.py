from tabulate import tabulate

def fillTableSing(PSNR_lsc, PSNR_he, PSNR_g,SSIM_lsc, SSIM_he, SSIM_g,i):
    data = [
        ["PSNR", PSNR_lsc,PSNR_he,PSNR_g],
        ["SSIM", SSIM_lsc,SSIM_he,SSIM_g]
        ]
    headers = ["METRICS","linear contrast stretching","histogram equalization", "denoising + gamma correction"]
    table = tabulate(data, headers, tablefmt="grid")
    return table
