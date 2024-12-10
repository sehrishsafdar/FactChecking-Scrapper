import csv
from scrappers.sochfactcheck.news_extractor import extract_details
from scrappers.sochfactcheck.crawl_all_news import scrape_all_pages


all_pages = scrape_all_pages()
all_articles = []


all_articles = extract_details(all_pages)

print('--- Data extracted from all pages! ---')

with open("soch_factcheck_articles.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Title", "Link", "Date", "Claim", "Image"])
    writer.writeheader() 
    writer.writerows(all_articles)