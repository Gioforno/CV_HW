from tabulate import tabulate


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
