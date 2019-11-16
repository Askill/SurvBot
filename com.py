import requests
import json
import config
import time
import cv2

login = config.loginPath
loginDataJson = {}
config.token
config.chat_id

def saveImage(img):
    name =  '{}'.format(int(time.time()))
    path = config.photos + name + '.png'
    cv2.imwrite(path, img)
    return path

def notify(path):
    global loginDataJson
    photo = open(path, "rb")
    json1 = {"chat_id": loginDataJson["chat_id"]}
    files = {'photo': photo}
    print(requests.post("https://api.telegram.org/bot" + loginDataJson["key"] + "/sendPhoto", json1, files=files))

def loadLogin():
    global loginDataJson
    with open(login,  'r', encoding='utf-8') as f:
        loginData = f.read()
        loginDataJson = json.loads(loginData)
        config.token = loginDataJson["key"]
        config.chat_id = loginDataJson["chat_id"] 

def initEndpoint():
    loadLogin()
    tp = "http://api.telegram.org/bot" + config.token + "/setWebHook?url=" + config.endpoint
    requests.get(tp)
    print("registered:", tp)



