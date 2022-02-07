import requests as rs
from bs4 import BeautifulSoup as bs
import re
import random as rd
import string 
i= input("please type in the package id: ")
r= rs.get("https://store.line.me/stickershop/product/{intt}/zh-Hant?page=1".format(intt= i))
soup= bs(r.text, "html.parser")

try: 
    name1= str(soup.find_all("span", {"class": "mdCMN09Image"}, limit= 1))
    print(str(name1))

    pattern= re.compile(r'(?<=\/)\d+(?=\/)')
    elementlist= re.findall(pattern, name1)
    element= int(elementlist[0])
    sidlist= [element+i for i in range(0, 24)]
    print(sidlist)
except: 
    print("qq")





