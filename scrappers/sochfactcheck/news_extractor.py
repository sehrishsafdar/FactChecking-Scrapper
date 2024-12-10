from bs4 import BeautifulSoup

def extract_details(all_pages, url=None):  # Default url to None
    articles = []

    for content in all_pages:
        soup = BeautifulSoup(content, "html.parser")
        article_boxes = soup.find_all('div', class_='article-box')
            
        for article_box in article_boxes:
            article_title = article_box.find('h6')  
            article_link_tag = article_box.find('a', href=True)  
            article_date = article_box.find(class_='article-date') 
            article_claim = article_box.find(class_='article_excerpt')

            # Initialize image_url to None for each article
            image_url = None
            
            # Find the div with class 'featured-image' and extract image URL
            featured_div = article_box.find('div', class_='featured-image')
            if featured_div:
                img_tag = featured_div.find('img')
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']
            
            if article_title and article_link_tag:
                title = article_title.text.strip()
                link = article_link_tag['href'].strip()

                # Construct full link only if URL is provided
                full_link = url + link if url and link.startswith('/') else link
                
                # Check if the date was found
                date = article_date.text.strip() if article_date else 'Unknown'  # Default to 'Unknown' if date is missing
                claim = article_claim.text.strip() if article_claim else 'No claim available'

                # Append the article details including the image URL to the articles list
                articles.append({
                    "Title": title,
                    "Link": full_link,
                    "Date": date,
                    "Claim": claim,
                    "Image": image_url  # Store the image URL here
                })

    return articles