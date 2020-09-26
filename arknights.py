from imgProcess import moveToImg
from cur import *
import os
import utils


sleep(3)

def login():
    imgPath = os.path.join("arkPic", "login.png")
    success = moveToImg(imgPath)
    if not success:
        return
    sleep(1)

    leftClick()
    sleep(3)

    imgPath = os.path.join("arkPic", "password.png")
    success = moveToImg(imgPath)
    if not success:
        return
    sleep(1)
    leftClick()
    sleep(2)

    typeString(utils.PASSWORD)
    typeChr("enter")

    imgPath = os.path.join("arkPic", "loginFinal.png")
    success = moveToImg(imgPath)
    if not success:
        return
    sleep(1)
    leftClick()

login()

