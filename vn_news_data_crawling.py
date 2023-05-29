import pandas as pd
import os
import requests
import time
import random

from io import BytesIO
from PIL import Image
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize edge browser
edge_option = webdriver.EdgeOptions()
edge_option.add_argument('--no-sandbox')
driver = webdriver.Edge(options=edge_option)

# Create a folder to storing articles (corpus)
root_dir = './vn_news_corpus'
os.makedirs(root_dir, exist_ok=True)

#Crawling
n_pages = 10 # Change if you want more articles
article_id = 0

for page_idx in tqdm(range(n_pages)):
    # Acess to table page
    main_url = f'https://vietnamnet.vn/thoi-su-page{page_idx}'
    driver.get(url=main_url)

    # Get list of articles (list of URLS)
    new_lst_xpath = '//div[@class="topStory-15nd"]/div/div[1]/a'
    new_tags = driver.find_elements(By.XPATH, new_lst_xpath)

    new_page_urls = [new_tag.get_attribute('href') for new_tag in new_tags]

    for new_page_url in new_page_urls:
        # Acess to article page
        driver.get(new_page_url)
        time.sleep(1)

        # Try to get main content tag
        main_content_xpath = '//div[@class="content-detail"]'
        try:
            main_content_tag = driver.find_element(By.XPATH, main_content_xpath)
        except:
            continue

        # Ignore if find video article
        video_content_xpath = '//div[@class="video-detail"]'
        try:
            video_content_tag = main_content_tag.find_element(By.XPATH, video_content_xpath)
            continue
        except:
            pass

        # Get title (h1 tag)
        title = main_content_tag.find_element(By.TAG_NAME, 'h1').text.strip()

        # Get abstract (h2 tag)
        abtract = main_content_tag.find_element(By.TAG_NAME, 'h2').text.strip()

        # Get author name (span tag)
        try:
            author_xpath = '//span[@class="name"]'
            author = main_content_tag.find_element(By.XPATH, author_xpath).text.strip()
        except:
            author = ''

        # Get paragraphs (all p tags in div "maincontent main-content)
        paragraph_xpath = '//div[@class="maincontent main-content"]/p'
        paragraph_tags = main_content_tag.find_elements(By.XPATH, paragraph_xpath)
        paragraph_lst = [paragraph_tag.text.strip() for paragraph_tag in paragraph_tags]
        paragraphs = ' '.join(paragraph_lst)

        # Combine title, abstract, author and paragraph
        final_content_lst = [title, abtract, paragraphs, author]
        final_content = '\n\n'.join(final_content_lst)

        # Save to file.txt
        article_filename = f'Article_{article_id:05d}.txt'
        article_savepath = os.path.join(root_dir, article_filename)
        article_id += 1

        with open(article_savepath, 'w', encoding='utf8') as f:
            f.write(final_content)

        # Move back to previous page
        driver.back()




























































































