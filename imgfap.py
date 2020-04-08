import urllib.request
import re
import os
import time

URL = ""
pnum = ""
imglist = ""


def mainLoop():
    global URL
    global pnum

    URL = input("Please input the gallery url: ")
    url = "www.imagefap.com/pictures/"
    galleryId = URL.split(url)[-1]
    galleryId = galleryId.split("/")[0]
    URL = F"https://{url}{galleryId}/?grid={galleryId}&view=2"
    validate(URL)
    
def validate(URL):
    print("Processing...")
    try:
        html = urllib.request.urlopen(URL).read()
    except Exception as e:
        print(f"Unexpected Error for {URL}: {e}")
        time.sleep(5)
        return
    getImages(html)

def getImages(html):
    global imglist
    imglist = re.findall('<td id="([0-9]+)" align="center"  ?valign="top">', str(html))
    imglist2 = []
    for image in imglist:
        url = "http://www.imagefap.com/photo/{}/".format(image)
        html =  urllib.request.urlopen(url).read()
        imglist2.append(re.findall('"contentUrl": "(.*?)",', str(html)))
        print("Processed {}/{}".format(str(len(imglist2)), str(len(imglist))))
    download(imglist2)
    

def download(urls):
    image = urls[0]
    image = image[0]
    dir_name = "Downloaded_imagefap"
    try:
        os.mkdir(dir_name)
    except:
        pass
    print("Downloading {} images".format(str(len(urls))))
    for image in urls:
        image = str(image[0])
        name = image.split("/")[-1].split("?end")[0]
        with urllib.request.urlopen(image) as f:
            imageContent = f.read()
            with open(f"{dir_name}/{name}", "wb") as f:
                f.write(imageContent)
    
        
mainLoop()

