from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
path = "chromedriver.exe"

wd = webdriver.Chrome(path)

url = "https://www.mytek.tn/informatique/ordinateurs-portables/pc-gamer.html"

def get_images_from_mytek(wd,delay,max_images,url=url):
    def scrolldown(wd,delay):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
        
    wd.get(url)
    image_urls= []
    thumbnails = []
    while len(image_urls) < max_images : 
        print("GETTING IMAGES ...............")
        scrolldown(wd, delay)
        thumbnails = wd.find_elements(By.CLASS_NAME,"product-image-photo")
        for image in thumbnails[len(image_urls):max_images]:
            if image.get_attribute('src') and "http" in image.get_attribute('src') : 
                image_url = image.get_attribute('src')
                image_urls.append(image_url)
    print(image_urls)
    return image_urls
    



def download_image(download_path,url,file_name):
    try : 
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        with open(file_path,"wb") as f : 
            image.save(f,'JPEG')
        print('================')
        print(f" {url} : DONE")
    except Exception as E : 
        print('================')
        print('Failed ',E)
        


download_image("./images/","https://mk-media.mytek.tn/media/catalog/product/cache/4635b69058c0dccf0c8109f6ac6742cc/8/1/81y4018qfe.jpg","test.jpg")

image_urls = get_images_from_mytek(wd,1,10)
for i in range(len(image_urls)):
    download_image("./images/",image_urls[i],f"{i}.jpg")
print('ALLL DONE !!!!!!!!!!!!!')
    