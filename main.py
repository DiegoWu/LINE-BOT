from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json 
import re
import aiohttp 
import asyncio 
from bs4 import BeautifulSoup as bs
import random as rd
import string  

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('5OpClASIe7+VGcheUVYzx6dVHp9q3FYIvCcN2BoNfgmGkNbZE64T/ffVao8y3z52efnJQ5Z+3KkM+r8et6WfjJbNkcfqkYQT2pwN4UR1bOZ940kY8DdKSviLRNXKQk5/Deq7R9wd/NKRUMcgKBzgZwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5033959d062d929efa452602b1a29efc')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'
    
# custom crawler 
async def custom_crawler(pkg):   
    global sidnumlist
    global coverlist
    global headerlist
    global sidelement
    global anilist 
    rr= await aiohttp.requests.get("https://store.line.me/stickershop/product/{intt}/zh-Hant?page=1".format(intt= pkg))
    soup= bs(rr.text, "html.parser")
    name1= str(soup.find_all("span", {"class": "mdCMN09Image"}))
    name2= str(soup.find_all("div", {"class": "mdCMN38Img"}, limit= 1))
    cover= str(soup.find_all("img", {"class": "FnImage"}, limit= 1))
    header= str(soup.find_all("p", {"class": "mdCMN38Item01Ttl"}, limit= 1))
    pattern= re.compile(r'(?<=\/)\d+(?=\/)')
    ppatern= re.compile(r'type" : .+"id":?')
    sidpattern= re.compile(r'(?:http.+png:?)')
    coverpattern= re.compile(r'(?:http.+true:?)')
    headerpattern= re.compile(r'(?:>.+<:?)')
    sidnumlist= re.findall(pattern, name1)
    sidelement= re.findall(sidpattern, name1)
    coverlist= re.findall(coverpattern, cover)
    headerlist= re.findall(headerpattern, header)
    anilist= re.findall(ppatern, name2)

#new_crawler

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

# following newest_crawler 
async def following_newest_crawler():
    async with aiofiles.open("latest.json",'r',encoding='utf-8') as load_f:
        load_dict= json.load(load_f)
        for i in range(len(tlelist)): 
            load_dict['contents'][0]['body']['contents'][i]['url']= tlelist[i][0]
        for i in range(11): 
            load_dict['contents'][i+1]['hero']['url']= coverlist[i][0]
            load_dict['contents'][i+1]['hero']['action']['uri']= "https://store.line.me/stickershop/product/{intt}/zh-Hant?page=1".format(intt=numberlist[i][0])
            load_dict['contents'][i+1]['body']['contents'][0]['text']= headerlist[i][0]
            load_dict['contents'][i+1]['footer']['contents'][0]['action']['Text']= "custom_"+numberlist[i][0]
        async with aiofiles.open("latest.json", 'w', encoding= 'utf-8') as f:
                
                json.dump(load_dict, f, ensure_ascii= False)

#follow event 
@handler.add(FollowEvent)
def handle_follow(event):

    publish= '''Hello, 我是貼圖小小葉，本名是宮水五葉😚請用「小小葉」或「貼圖葉」喚醒我！將我加入群組或群聊，或許可以使群組充滿歡樂的氣氛🧐😝
             '''
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text= publish))

# join event 
@handler.add(JoinEvent)
def handle_join(event):

    publish= '''Hello everyone, 我是貼圖小小葉，本名是宮水五葉😚請用我的小名「小小葉」或「貼圖葉」喚醒我! 希望我能快速融入你們><
             '''
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text= publish))

#postback event 
@handler.add(PostbackEvent)
def handle_postback(event):
    data= event.postback.data

    if data== 'tipss':
    
        instruction= json.load(open('tips.json','r'))
        FlexMessage= FlexSendMessage( 
            alt_text= '指令教學',
            contents= instruction
        )
        line_bot_api.reply_message(event.reply_token, FlexMessage)

    elif data== 'identification':

        prf= json.load(open('id.json','r'))
        FlexMessage= FlexSendMessage(
            alt_text= '作者簡介', 
            contents= prf
        )
        line_bot_api.reply_message(event.reply_token, FlexMessage)


    elif data== 'fixing': 
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= "尚未完工QQ"))

    elif data== 'new':

        newest_crawler()

        following_newest_crawler()

        new= json.load(open('latest.json','r'))
        FlexMessage= FlexSendMessage( 
            alt_text= "最新上架",
            contents= new
        )
        line_bot_api.reply_message(event.reply_token, FlexMessage)

    elif data== 'random':
        
        newest_crawler()

        pkgg= numberlist[rd.randint(0, 10)][0]
        
        custom_crawler(pkgg)
        
        v= [] # url for users 
        for i in range(0, int(len(sidnumlist)), 2):
            if len(anilist[0])>= 23:  
                v.append("line://app/1602687308-GXq4Vvk9?type=sticker&stk=anim&sid={}&pkg={}".format(sidnumlist[i], pkgg))
            else: 
                v.append("line://app/1602687308-GXq4Vvk9?type=sticker&stk=noanim&sid={}&pkg={}".format(sidnumlist[i], pkgg))
        length= len(sidnumlist)/8

        with open("custom_{}.json".format(int(len(sidnumlist)/2)),'r',encoding='utf-8') as load_f:
                    
            load_dict= json.load(load_f)
            load_dict['hero']['url']= coverlist[0]
            load_dict['hero']['action']['uri']= "https://store.line.me/stickershop/product/{intt}/zh-Hant?page=1".format(intt= pkgg)
            load_dict['header']['contents'][0]['text']= headerlist[0]
            count= 0

            for i in range(int(length)):
                for j in range(4): 
                    load_dict['body']['contents'][i]['contents'][j]['action']['uri']= v[count]
                    count+= 1
            
            with open("custom_{}.json".format(int(len(sidnumlist)/2)),'w',encoding='utf-8') as f:

                json.dump(load_dict, f, ensure_ascii=False)
        
        cst= json.load(open("custom_{}.json".format(int(len(sidnumlist)/2)),'r'))
        FlexMessage= FlexSendMessage(
            alt_text= 'custom', 
            contents= cst
        )  
        line_bot_api.reply_message(event.reply_token, FlexMessage)


# Message event
@handler.add(MessageEvent)
def handle_message(event):
    
    pkg= ""
    sid= ""
    message_type = event.message.type 
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message
    #profile = line_bot_api.get_profile(user_id)
    '''
    print(type(profile))
    with open("userid.json", 'w', encoding='utf-8') as u:
        json.dump(profile, u, ensure_ascii=False)
    uuserid= json.load(open('userid.json','r'))
    print(uuserid)
    '''

    if message_type== 'text': # text preprocessing 
        print(message.text)
        chrc= any(chr.isalpha() for chr in message.text)

        if message.text.lower() == 'profile' :

            print("profile")

        elif message.text.lower()== '小小葉' or message.text.lower()== '貼圖葉': 

            print("wow")

        elif message.text.lower()[0:6]== 'custom' or str(message.text).find('https://line.me/S/sticker/')!= -1 or str(message.text).find('https://store.line.me/stickershop/')!= -1: 
            print('custom')
            cstpattern= re.compile('\d+')
            pkglist= re.findall(cstpattern, str(message.text))
            pkg= ""
            for i in range(len(pkglist)): 
                if len(pkglist[i])> len(pkg): 
                    pkg= pkglist[i]
        
        elif message.text.lower()[0:6]==  'latest'or message.text.lower()[0:6]== 'newest' or message.text.lower()[0:4]== "最新上架":
            
            print("hi")

        elif message.text.lower()[0:6]!=  "custom" and chrc : 

            print("not my business")

        elif message.text== 'random':

            print("random")

        else:

            pkg= message.text

    elif message_type== 'sticker': # sticker preprocessing 

        # getting pkg id method 1

        message_pkg= message.package_id
        message_sid= message.sticker_id

        # getting pkg id method 2 (currently in use)

        pattern= re.compile(r'packageId": "(\d+:?)')
        patternsid= re.compile(r'stickerId": "(\d+:?)')
        elementr= re.findall(pattern, str(message))
        elements= re.findall(patternsid, str(message))
        pkg= elementr[0]
        sid= elements[0]

        print("pkg_num: ", pkg)
    
    if message.text.lower()== '小小葉' or message.text.lower()== '貼圖葉': 

        cnt= json.load(open("mainpage.json"))
        FlexMessage= FlexSendMessage(
            alt_text= 'mainpage', 
            contents= cnt
        )  
        line_bot_api.reply_message(reply_token, FlexMessage)

    elif message.text.lower() == 'profile' :

        prf= json.load(open('id.json','r'))
        FlexMessage= FlexSendMessage(
            alt_text= 'hello', 
            contents= prf
        )
        line_bot_api.reply_message(reply_token, FlexMessage)

    elif pkg!= "": 

        custom_crawler(pkg) 

        if len(sidnumlist)== 0 and sid!="":  

            sticker_message = StickerSendMessage(package_id=pkg,sticker_id=sid)
            line_bot_api.reply_message(reply_token, sticker_message)
    
        else: 
            
            v= [] # url for users 
            for i in range(0, int(len(sidnumlist)), 2):
                if len(anilist[0])>= 23:  
                    v.append("line://app/1602687308-GXq4Vvk9?type=sticker&stk=anim&sid={}&pkg={}".format(sidnumlist[i], pkg))
                else: 
                    v.append("line://app/1602687308-GXq4Vvk9?type=sticker&stk=noanim&sid={}&pkg={}".format(sidnumlist[i], pkg))
            length= len(sidnumlist)/8
            #print(length)
            if message.text.lower()[0:6]== 'custom' or str(message.text).find('https://line.me/S/sticker/')!= -1 or  str(message.text).find('https://store.line.me/stickershop/')!= -1: 

                with open("custom_{}.json".format(int(len(sidnumlist)/2)),'r',encoding='utf-8') as load_f:
                    
                    load_dict= json.load(load_f)
                    load_dict['hero']['url']= coverlist[0]
                    load_dict['hero']['action']['uri']= "https://store.line.me/stickershop/product/{intt}/zh-Hant?page=1".format(intt= pkg)
                    load_dict['header']['contents'][0]['text']= headerlist[0]
                    count= 0
    
                    for i in range(int(length)):
                        for j in range(4): 
                            load_dict['body']['contents'][i]['contents'][j]['action']['uri']= v[count]
                            count+= 1
                    
                    with open("custom_{}.json".format(int(len(sidnumlist)/2)),'w',encoding='utf-8') as f:

                        json.dump(load_dict, f, ensure_ascii=False)
                
                cst= json.load(open("custom_{}.json".format(int(len(sidnumlist)/2)),'r'))
                FlexMessage= FlexSendMessage(
                    alt_text= 'custom_sticker', 
                    contents= cst
                )  
                line_bot_api.reply_message(reply_token, FlexMessage)

            else: 

                sidurl= sidelement[0]
                image_message = ImageSendMessage(
                original_content_url=sidurl,
                preview_image_url=sidurl
                )
                line_bot_api.reply_message(reply_token, image_message)

    elif message.text.lower()[0:6]==  'latest'or message.text.lower()[0:6]== 'newest' or message.text.lower()[0:4]== "最新上架": 

        newest_crawler()

        following_newest_crawler()

        new= json.load(open('latest.json','r'))
        FlexMessage= FlexSendMessage(
            alt_text= '最新上架', 
            contents= new
        )
        line_bot_api.reply_message(reply_token, FlexMessage)

    elif message.text== 'random': 

        newest_crawler()

        pkgg= numberlist[rd.randint(0, 10)][0]
        
        custom_crawler(pkgg)
        
        v= [] # url for users 
        for i in range(0, int(len(sidnumlist)), 2):
            if len(anilist[0])>= 23:  
                v.append("line://app/1602687308-GXq4Vvk9?type=sticker&stk=anim&sid={}&pkg={}".format(sidnumlist[i], pkgg))
            else: 
                v.append("line://app/1602687308-GXq4Vvk9?type=sticker&stk=noanim&sid={}&pkg={}".format(sidnumlist[i], pkgg))
        length= len(sidnumlist)/8

        with open("custom_{}.json".format(int(len(sidnumlist)/2)),'r',encoding='utf-8') as load_f:
                    
            load_dict= json.load(load_f)
            load_dict['hero']['url']= coverlist[0]
            load_dict['hero']['action']['uri']= "https://store.line.me/stickershop/product/{intt}/zh-Hant?page=1".format(intt= pkgg)
            load_dict['header']['contents'][0]['text']= headerlist[0]
            count= 0

            for i in range(int(length)):
                for j in range(4): 
                    load_dict['body']['contents'][i]['contents'][j]['action']['uri']= v[count]
                    count+= 1
            
            with open("custom_{}.json".format(int(len(sidnumlist)/2)),'w',encoding='utf-8') as f:

                json.dump(load_dict, f, ensure_ascii=False)
        
        cst= json.load(open("custom_{}.json".format(int(len(sidnumlist)/2)),'r'))
        FlexMessage= FlexSendMessage(
            alt_text= 'custom', 
            contents= cst
        )  
        line_bot_api.reply_message(event.reply_token, FlexMessage)
     
import os
if __name__ == "__main__":
    #asyncio.run(main)
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)  
