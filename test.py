import requests 
from bs4 import BeautifulSoup as bs
import random as rd
import re
from PIL import Image
import matplotlib.pyplot as plt
import os
import aiohttp
import asyncio

async def newest_crawler(): 
    global tlelist
    global coverlist
    global headerlist
    global newlist
    global numberlist
    ttemp= []
    tttemp= []
    ttttemp= []
    tempnumber= []
    tt= []
    r= await aiohttp.requests.get("https://store.line.me/home/zh-Hant")
    soup=  bs(r.text, "html.parser")
    name1= (soup.find_all("div", {"class": "mdCMN03Img"} ))
    name2= (soup.find_all("li", {"class": "mdMN04Li"}) )
    pattern= re.compile(r'(?:https.+pc:?)')
    elepattern= re.compile(r'(https:\/\/store.+stickershop/product\/\d+:?)')
    elepattern1= re.compile(r'(\/stickershop\/.+Hant)')
    numberpattern= re.compile(r'\/\d+\/')
    for ele in name1: 
        tt.append(re.findall(pattern, str(ele)))
    tlelist= tt 
    elelist= re.findall(elepattern, str(name1))
    elelist1= re.findall(elepattern1, str(name2))
    for ele in elelist1: 
        ele= "https://store.line.me/"+ ele
        ttemp.append(ele)
    newlist= ttemp+ elelist
    for ele in newlist: 
        r= await aiohttp.requests.get(ele)
        soup= bs(r.text, "html.parser")
        cover= str(soup.find_all("img", {"class": "FnImage"}, limit= 1))
        header= str(soup.find_all("p", {"class": "mdCMN38Item01Ttl"}, limit= 1))
        coverpattern= re.compile(r'(?:http.+true:?)')
        headerpattern= re.compile(r'(?:>.+<:?)')
        tttemp.append(re.findall(coverpattern, cover))
        ttttemp.append(re.findall(headerpattern, header))
        temp= re.findall(numberpattern, str(re.findall(coverpattern, cover))) 
        temp[0]= temp[0].replace("/", "")
        tempnumber.append(temp)
    coverlist= tttemp
    headerlist= ttttemp 
    numberlist= tempnumber
    print(numberlist)
asyncio.run(newest_crawler())

r= requests.get('https://store.line.me/stickershop/product/11365154/zh-Hant')
soup= bs(r.text, "html.parser")
name1= str(soup.find_all("div", {"class": "mdCMN09ImgList"}, limit= 1))
pattern= re.compile(r'(data-widget=".[^"]+:?)')
comlist= re.findall(pattern, name1)
print (comlist)
if len(comlist[0])== 33:

    name2= str(soup.find_all("img", {"class": "mdCMN38ImgOver FnCustomOverlay"}))
    #mm= soup.select("document.querySelector(\"body > div.LyWrap > div > div.LyMain > section > div.mdBox03Inner01 > div.MdCMN09DetailView.mdCMN09Sticker > div.mdCMN09ImgList > div.mdCMN09ImgListWarp > ul > li:nth-child(3) > div.mdCMN09LiInner.FnImage > span.mdCMN09Image.mdCMN09Over.FnCustomOverlay\")")
   # print(mm)
    print(name2)
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