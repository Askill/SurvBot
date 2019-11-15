import requests
import json
import telebot
import numpy as np
import cv2

import time

login = "./data.json"
loginDataJson = {}

photos = "./imgs/"
url = "http://192.168.178.25:8000/stream.mjpg"

def checkCam():
    cap = cv2.VideoCapture(url)
    r, img = cap.read()
    return img

def saveImage(img):
    name =  '{0:010x}'.format(int(time.time() * 256))[:10]
    path = photos + name + '.png'
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

loadLogin()

