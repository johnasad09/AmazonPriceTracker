import os
from dotenv import load_dotenv
import smtplib
import requests
from bs4 import BeautifulSoup

load_dotenv()

AMAZON_URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]
RECIPIENT_EMAIL = "abc@mail.com"
# --------------------------------------------------------------
def send_mail(msg):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIPIENT_EMAIL, msg=msg)

# -------------------------------------------------------------
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    }

response = requests.get(url=AMAZON_URL, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")
price = soup.find(name="span", class_="a-offscreen").get_text()

price_without_symbol = float(price.split("$")[1])
print(price_without_symbol)
target_price = 100

title = soup.find(id="productTitle").get_text().strip()
print(title)

if price_without_symbol <= target_price:
    message = f"{title} is on sale for {price}!"
    msg = f"Subject:Amazon Price Alert!\n\n{message}\n{AMAZON_URL}".encode("utf-8")
    send_mail(msg)
    

