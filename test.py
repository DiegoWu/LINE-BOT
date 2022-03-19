import requests 
from bs4 import BeautifulSoup as bs
import random as rd
import re
from PIL import Image
import matplotlib.pyplot as plt
import os


r= requests.get('https://store.line.me/stickershop/product/11365154/zh-Hant')
soup= bs(r.text, "html.parser")
name1= str(soup.find_all("div", {"class": "mdCMN09ImgList"}, limit= 1))
pattern= re.compile(r'(data-widget=".[^"]+:?)')
comlist= re.findall(pattern, name1)

if len(comlist[0])== 33:

    name2= str(soup.find_all("img", {"class": "mdCMN38ImgOver FnCustomOverlay"}))
    mm= soup.select("document.querySelector(\"body > div.LyWrap > div > div.LyMain > section > div.mdBox03Inner01 > div.MdCMN09DetailView.mdCMN09Sticker > div.mdCMN09ImgList > div.mdCMN09ImgListWarp > ul > li:nth-child(3) > div.mdCMN09LiInner.FnImage > span.mdCMN09Image.mdCMN09Over.FnCustomOverlay\")")
    print(mm)
    #print(name2)
    #npattern= re.compile(r'')
    name3= str

'''
# 載入兩張影像
img1 = Image.open("image1.jpg")
img2 = Image.open("image2.jpg")

# 檢查兩張影像大小是否一致
print(img1.size)
print(img2.size)

# 指定目標圖片大小
imgSize = (720, 480)

# 改變影像大小
img1.resize(imgSize)
img2.resize(imgSize)

# 指定裁切大小
cropBox = (
    0,   # left
    0,   # upper
    720, # right
    480  # lower
)

# 裁切影像
img1.crop(cropBox)
img2.crop(cropBox)

blendImg = Image.blend(img1, img2, alpha = 0.5)

# 顯示影像
blendImg.show()
'''