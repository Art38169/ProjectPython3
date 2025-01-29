import requests
from bs4 import BeautifulSoup
import os

def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def get_image_url(website_url):
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img')  # You may want to adjust this depending on the structure of the webpage
    return img_tag['src'] if img_tag else None

instagram_url = 'https://gs.statcounter.com/social-media-stats/all/thailand'  # Replace with the actual website URL
img_url = get_image_url(instagram_url)
if img_url:
    download_image(img_url, 'image.png')


