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
    json1 = {"chat_id": config.chat_id}
    files = {'photo': photo}
    print(requests.post("https://api.telegram.org/bot" + config.token + "/sendPhoto", json1, files=files))


def initEndpoint():
    tp = "http://api.telegram.org/bot" + config.token + "/setWebHook?url=" + config.endpoint
    requests.get(tp)
    print("registered:", tp)



