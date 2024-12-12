from bs4 import BeautifulSoup
from utils.datetime_util import convert_to_datetime
from utils.string_util import title_to_file_name
import requests
from PIL import Image
from io import BytesIO
import os

def get_image_from_url(image_url):
    
    response = requests.get(image_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        return image   
            
def extract_one_page(content, url=None):
        
        articles = []

        soup = BeautifulSoup(content, "html.parser")
        article_boxes = soup.find_all('div', class_='article-box')
            
        for article_box in article_boxes:
            article_title = article_box.find('h6')  
            article_link_tag = article_box.find('a', href=True)  
            article_date = article_box.find(class_='article-date') 
            article_claim = article_box.find(class_='article_excerpt')
            #article_label = article_box.find(class_ ='label')
            #article_label = article_box.find('span', class_='label')
            article_label = article_box.find('div', class_='show-label')
            # Initialize image_url to None for each article
            image_url = None
            
            # Find the div with class 'featured-image' and extract image URL
            featured_div = article_box.find('div', class_='featured-image')
            
            title = ''

            if article_title and article_link_tag:
                title = article_title.text.strip()
            
            if featured_div:
                img_tag = featured_div.find('img')
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']
                    retrieved_image = get_image_from_url(image_url)
                    file_name = title_to_file_name(title)
                    save_path = os.path.join("sochfactcheck", file_name)
                                  
                    retrieved_image.save(save_path)


            link = article_link_tag['href'].strip()

                # Construct full link only if URL is provided
            full_link = url + link if url and link.startswith('/') else link
                
                # Check if the date was found
            date = article_date.text.strip() if article_date else 'Unknown'  # Default to 'Unknown' if date is missing
            claim = article_claim.text.strip() if article_claim else 'No claim available'
                #label = article_label.text.strip()
            label = article_label.text.strip()
 
            convereted_date = convert_to_datetime(date)

                # Append the article details including the image URL to the articles list
            articles.append({
                    "Title": title,
                    "Link": full_link,
                    "Date": convereted_date,
                    "Claim": claim,
                    "Label": label,
                    "Image": image_url  
                })

        return articles

def extract_details(all_pages, url=None):  # Default url to None
    
    all_articles = []

    for content in all_pages:
        all_articles = all_articles + extract_one_page(content)

    return all_articles