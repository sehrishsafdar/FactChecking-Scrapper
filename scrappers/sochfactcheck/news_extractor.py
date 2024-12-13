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
    return None

def extract_one_page(content, url=None):
    
    articles = []

    soup = BeautifulSoup(content, "html.parser")
    article_boxes = soup.find_all('div', class_='article-box')

    for article_box in article_boxes:
        article_title = article_box.find('h6')
        article_link_tag = article_box.find('a', href=True)
        article_date = article_box.find(class_='article-date')
        article_claim = article_box.find(class_='article_excerpt')
        article_label_html = article_box.find('div', class_='show-label')  # HTML label element
        label_from_html = article_label_html.text.strip() if article_label_html else None

        # Initialize variables
        image_url = None
        image_label = None

        # Extract title
        title = article_title.text.strip() if article_title else ''

        # Extract featured image
        featured_div = article_box.find('div', class_='featured-image')
        if featured_div:
            img_tag = featured_div.find('img')
            if img_tag and img_tag.get('src'):
                image_url = img_tag['src']

                # Fetch and save the image
                retrieved_image = get_image_from_url(image_url)
                if retrieved_image:
                    image_rgb = retrieved_image.convert("RGB")
                    file_name = title_to_file_name(title)
                    save_path = os.path.join("sochfactcheck", file_name)

                    # Ensure valid file extension
                    if not save_path.endswith(('.png', '.jpg', '.jpeg')):
                        save_path += '.png'

                    # Save the image
                    image_rgb.save(save_path)

                    # Get label from the image
                    from utils.extract_label_from_image import get_image_label  # Local import to avoid circular dependency
                    image_label = get_image_label(save_path)

        # Extract article link
        link = article_link_tag['href'].strip() if article_link_tag else ''
        full_link = url + link if url and link.startswith('/') else link

        # Extract claim
        claim = article_claim.text.strip() if article_claim else 'No claim available'

        # Extract and convert date
        date = article_date.text.strip() if article_date else 'Unknown'
        converted_date = convert_to_datetime(date)

        # Decide the label: prefer image-derived label if available
        label = image_label if image_label else label_from_html

        # Append article details
        articles.append({
            "Title": title,
            "Link": full_link,
            "Date": converted_date,
            "Claim": claim,
            "Label": label,
            "Image": image_url
        })

    return articles

def extract_details(all_pages, url=None):
    
    all_articles = []

    for content in all_pages:
        all_articles += extract_one_page(content, url)

    return all_articles
