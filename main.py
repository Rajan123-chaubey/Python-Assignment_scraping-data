import requests
from bs4 import BeautifulSoup
import csv




base_url = "https://www.amazon.in/s"
search_query = "bags"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


#Scrape the 20 product pages:

for page in range(1, 21):  
    link = {
        "k": search_query,
        "crid": "2M096C61O4MLT",
        "qid": "1653308124",
        "sprefix": "ba%2Caps%2C283",
        "ref": f"sr_pg_{page}",
        "page": page
    }

    response = requests.get(base_url, headers=headers, params=link)
       
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all("div", class_="sg-col-inner")

    data = []

    for product in products:
        product_url = product.find("a", class_= "a-link-normal").get("href")
        product_name = product.find("span", class_="a-size-base-plus").text.strip()
        product_price = product.find("span", class_="a-offscreen").text.strip()
        rating = product.find("span", class_="a-icon-alt").text.strip()
        num_reviews = product.find("span", class_="a-size-base").text.strip()

        data.append([product_url, product_name, product_price, rating, num_reviews])

    


#Scrape single pages:

for item in data:
    product_url = item[0]

    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    description = soup.find("div", id="feature-bullets").text.strip()
    asin = soup.find("th", text="ASIN").find_next_sibling("td").text.strip()
    product_description = soup.find("div", id="productDescription").text.strip()
    manufacturer = soup.find("th", text="Manufacturer").find_next_sibling("td").text.strip()

    item.extend([description, asin, product_description, manufacturer])

    

#Save as CSV file:

with open("scraped_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews",
                     "Description", "ASIN", "Product Description", "Manufacturer"])
    writer.writerows(data)


