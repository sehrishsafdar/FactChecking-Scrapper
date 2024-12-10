import requests
from bs4 import BeautifulSoup
import csv

# URL of the SOCH FactCheck website
url = "https://www.sochfactcheck.com/"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    article_boxes = soup.find_all('div', class_='article-box')
    articles = []
    for article_box in article_boxes:
        article_title = article_box.find('h6')  
        article_link_tag = article_box.find('a', href=True)  
        article_date = article_box.find(class_='article-date') 
        article_claim = article_box.find(class_='article_excerpt')
        image = article_box.find(class_='featured_image') 

        if article_title and article_link_tag:
            title = article_title.text.strip()
            link = article_link_tag['href'].strip()  
            full_link = url + link if link.startswith('/') else link  
            
            # Check if the date was found
            date = article_date.text.strip() if article_date else 'Unknown'  # Default to 'Unknown' if date is missing
            claim = article_claim.text.strip()
            articles.append({
                "Title": title,
                "Link": full_link,
                "Date": date,
                "claim": claim,
                "image": image
            })

            print(f"Title: {title}")
            print(f"Link: {full_link}")
            print(f"Date: {date}")
            print(f"claim: {claim}")
            print(f"image: {image}")
            print("-" * 50)
    with open("soch_factcheck_articles.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Title", "Link", "Date", "claim", "image"])
        writer.writeheader() 
        writer.writerows(articles) 

    print(f"Scraped {len(articles)} articles. Data saved to 'soch_factcheck_articles.csv'.")
else:
    print(f"Failed to fetch the website. Status code: {response.status_code}")
